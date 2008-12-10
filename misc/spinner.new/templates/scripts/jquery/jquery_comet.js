(function($)
{
	var msgHandshake =
	{
		version: '1.0',
		minimumVersion: '0.9',
		channel: '/meta/handshake'
	};

	var msgConnect =
	{
		channel: '/meta/connect',
		connectionType: 'long-polling'
	};

	var msgSubscribe =
	{
		channel: '/meta/subscribe'
	};

	var msgUnsubscribe =
	{
		channel: '/meta/unsubscribe'
	};

	var msgDisconnect =
	{
		channel: '/meta/disconnect'
	};


	var oTransport =
	{
		connectionType: 'long-polling',

		startup: function(oReturn)
		{
			if(this._comet._bConnected) return;
			this.tunnelInit();
		},

		tunnelInit: function()
		{
			var msgConnect = 
			{
				channel: '/meta/connect',
				clientId: $.comet.clientId, 
				id: $.comet._nNextId++,
				connectionType: $.comet._oTransport.connectionType
			};
			this.openTunnel({message: JSON.stringify(msgConnect)});
		},

		openTunnel: function(oMsg)
		{
			$.comet._bPolling = true;

			$.ajax({
				url: $.comet._sUrl,
				data: oMsg,
				type: 'post',
				success: function(sReturn)
				{
					var oReturn = eval(sReturn);
					$.comet._bPolling = false;
					$.comet.deliver(oReturn);
					$.comet._oTransport.closeTunnel();
				}
			});
		},

		closeTunnel: function()
		{
			if(!$.comet._bInitialized) return;

			if($.comet._advice)
			{
				if($.comet._advice.reconnect == 'none') return;

				if($.comet._advice.interval > 0)
				{
					setTimeout($.comet._oTransport._connect, $.comet._advice.interval);
				}
				else
				{
					$.comet._oTransport._connect();
				}
			}
			else
			{
				$.comet._oTransport._connect();
			}
		},

		_connect: function()
		{
			if(!$.comet._bInitialized) return;

			if($.comet._bPolling) return;

			if($.comet._advice && $.comet._advice.reconnect == 'handshake')
			{
				$.comet._bConnected = false;
				$.comet.init($.comet._sUrl);
			}
			else if($.comet._bConnected)
			{
				var msgConnect = 
				{
					clientId: $.comet.clientId,
					id: $.comet._nNextId++,
					channel: '/meta/connect'
				};
				$.comet._oTransport.openTunnel({message: JSON.stringify(msgConnect)});
			}
		},

		_send: function(sUrl, oMsg, fCallback) {
			var fCallback = (fCallback) ? fCallback : function(sReturn)
			{
				var oReturn = eval(sReturn);
				$.event.trigger('/cometd/meta', [oReturn]);
			};

			$.ajax({
				url: sUrl,
				type: 'post',
				beforeSend: function(oXhr) { oXhr.setRequestHeader('Connection', 'Keep-Alive'); },
				data: { message: JSON.stringify(oMsg) },
				success: function(sReturn)
				{
					var oReturn = eval(sReturn);

					$.comet.deliver(oReturn);

					if($.comet._advice)
					{
						if($.comet._advice.reconnect == 'none')
							return;

						if($.comet._advice.interval > 0)
						{
							setTimeout($.comet._connect, $.comet._advice.interval);
						}
						else
						{
							$.comet._connect();
						}
					}
					else
					{
						$.comet._connect();
					}
				}
			});
		}
	};

	$.comet = new function()
	{
		this.CONNECTED = 'CONNECTED';
		this.CONNECTING = 'CONNECTING';
		this.DISCONNECTED = 'DISCONNECTED';
		this.DISCONNECTING = 'DISCONNECTING';

		this._aMessageQueue = [];
		this._aSubscriptions = [];
		this._bInitialized = false;
		this._bConnected = false;
		this._nBatch = 0;
		this._nNextId = 0;
		this._oTransport = oTransport;
		this._sUrl = '';


		this.clientId = '';

		this.init = function(sUrl)
		{
			this._sUrl = (sUrl) ? sUrl : '/cometd';

			this._aMessageQueue = [];
			this._aSubscriptions = [];
			this._bInitialized = true;
			this.startBatch();

			$.ajax({
				url: this._sUrl,
				type: 'post',
				beforeSend: function(oXhr) { oXhr.setRequestHeader('Connection', 'Keep-Alive'); },
				success: this._finishInit,
				data: { message: JSON.stringify($.extend(msgHandshake, {id: this._nNextId++ })) }
			});
		};

		this._finishInit = function(sReturn)
		{
			var oReturn = eval(sReturn)[0];

			if(oReturn.advice)
				$.comet._advice = oReturn.advice;
			
			var bSuccess = (oReturn.successful) ? oReturn.successful : false;

			// do version check

			if(bSuccess)
			{
				// pick transport ?
				// ......

				$.comet._oTransport._comet = $.comet;
				$.comet._oTransport.version = $.comet.version;

				$.comet.clientId = oReturn.clientId;
				$.comet._oTransport.startup(oReturn);
			}
		}

		this._sendMessage = function(oMsg)
		{
			if($.comet._nBatch <= 0)
			{
				if(oMsg.length > 0)
					for(var i in oMsg)
					{
						oMsg[i].id = $.comet._nNextId++;
						oMsg[i].clientId = $.comet.clientId;
					}
				else
				{
					oMsg.clientId = $.comet.clientId;
					oMsg.id = $.comet._nNextId++;
				}
				
				$.comet._oTransport._send($.comet._sUrl, oMsg);
			}
			else
				$.comet._aMessageQueue.push(oMsg);
		};

		this.startBatch = function() { this._nBatch++ };
		this.endBatch = function() {
			if(--this._nBatch == 0)
			{
				this._sendMessage(this._aMessageQueue);

				this._aMessageQueue = [];
			}
		};

		this.subscribe = function(sSubscription, fCallback)
		{
			// if this topic has not been subscribed to yet, send the message now
			if(!this._aSubscriptions[sSubscription])
			{
				this._aSubscriptions.push(sSubscription)
				this._sendMessage($.extend(msgSubscribe, { subscription: sSubscription }));
			}

			//$.event.add(this, sSubscription, fCallback);
		};

		this.unsubscribe = function(sSubscription) {
			$.comet._sendMessage($.extend(msgUnsubscribe, { subscription: sSubscription }));
		};

		this.publish = function(sChannel, oData)
		{
			$.comet._sendMessage({channel: sChannel, data: oData});
		};

		this.deliver = function(sReturn)
		{
			var oReturn = eval(sReturn);

			$(oReturn).each(function()
			{
				$.comet._deliver(this);
			});
		};

		this.disconnect = function()
		{
			$($.comet._aSubscriptions).each(function(i)
			{
				$.comet.unsubscribe($.comet._aSubscriptions[i]);
			});

			$.comet._sendMessage({channel:'/meta/disconnect'});

			$.comet._bInitialized = false;
		}

		this._deliver = function(oMsg,oData)
		{
			if(oMsg.advice)
			{
				$.comet._advice = oMsg.advice;
			}
			
			switch(oMsg.channel)
			{
				case '/meta/connect':
					if(oMsg.successful && !$.comet._bConnected)
					{
						$.comet._bConnected = $.comet._bInitialized;
						$.comet.endBatch();
						/*
						$.comet._sendMessage(msgConnect);
						*/
					}
					else
						//$.comet._bConnected = false;
				break;

				case '/meta/subscribe':
				break;

				case '/meta/unsubscribe':
				break;

			}

			if(oMsg.data)
			{
				$.event.trigger(oMsg.channel, [oMsg]);
			}
		};
	};

})(jQuery);

