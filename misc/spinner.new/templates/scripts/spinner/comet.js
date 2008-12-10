
MAX_REQUESTS 		= 10;
CURRENT_REQUEST	= 0;
sResults				= [];

function comet_getResults(sQuery) {

	if (CURRENT_REQUEST == MAX_REQUESTS) {
		return;
	}


	jQuery.get('/spinner/synonyms/', {'q': sQuery}, function( sData, sStatus ) {

		if( sStatus == 'success' ) {
						
			//	Check if there is new data
			if( sResults != sData ) {
				sResults	= sData;
				oData			= eval('('+sData+')');
				//	Logarithmic scale so the delay between 19->20 is longer than 1->2
				setTimeout('comet_getResults()', Math.log(Math.pow(++CURRENT_REQUEST * 1000, 50)));
				
				//	Trigger the load results event
				jQuery('#results').trigger('load_results', [oData]);
			
			}
			
		} else {
			alert('Error: ' + sStatus);
		}
	});
}

jQuery(document).ready(function(){
	
	//
	//	load_results()
	//
	//	Load the results back from the server if there are any
	//
	jQuery('#results').bind('load_results', function( oEvent, oData ) {
		
		if( CURRENT_REQUEST == 1 ) {
			jQuery('#results').text('');
		}
		for( var sWord in oData) {
					
			jQuery('#results').append(sWord +"<br/>");

			for( var sSyn in oData[sWord] ) {
				jQuery('#results').append(" -- " + oData[sWord][sSyn] +' - '+ sSyn + "<br/>");
			}

		}
	});	
});