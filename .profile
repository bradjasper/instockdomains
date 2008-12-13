export PATH=/opt/local/bin:/opt/local/sbin:$PATH
export PATH=/usr/local/mysql/bin:$PATH
export PATH=/usr/local/lib:$PATH
export PS1='\[\e[0;32m\]\u\[\e[m\] \[\e[1;34m\]\w\[\e[m\] \[\e[1;32m\]\$\[\e[m\]\[\e[1;37m\] '

ff () { find . -name \*.py | xargs grep "$1" | tr -d "\t"; }
function gvim { /Applications/MacVim.app/Contents/MacOS/Vim -g $*; }
change_path() { export PYTHONPATH=$BASE_PATH:$HOME/Sites/$1/; }
change_django() { unset DJANGO_SETTINGS_MODULE;  export DJANGO_SETTINGS_MODULE=$1.settings; } 
make_active() { change_path $1; change_django $1; }

alias ls='ls -G'
alias l='ls -G'
alias v='vim'

alias cdmamp='cd /Applications/MAMP/'
alias cdrcn='cd /Users/bjasper/Sites/rentacarnow/'
alias cdinst='cd /Users/bjasper/Sites/instockdomains/'
alias cdpython='cd /usr/local/lib/python2.6/site-packages'

alias flushhosts="sudo niload -v -m hosts ."
alias devsql='mysql -u bjasper -p mactips3'
alias pm='python manage.py'
alias maketags='ctags -R -f ~/.vim/tags/all.ctags ~/Sites/'
alias makepy=' rm -rf pydiction; python /Users/bjasper/.vim/pydiction.py rentacarnow.main rentacarnow.proxies rentacarnow.regions django '

export PYTHONPATH=/usr/local/lib/python2.5/site-packages/:$PYTHONPATH
export PYTHONPATH=$HOME/Sites/:$HOME/Sites/python/:$PYTHONPATH
export BASE_PATH=$PYTHONPATH
export ACTIVE_PROJECT=instockdomains

make_active 'rentacarnow'
