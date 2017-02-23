An IRC Bot Written in Python
==

### **pyBot Requirements:**###
>  * **Python 3.2 or higher**
>  * **BeautifulSoup 4**
>  * **Lxml or html5lib**
>  * **python-dateutil**
>  * **pystemmer (for Cobe)**
>  * **python3-selenium and phantomjs (for fmi.py)**

> _**Debian based distros:**_
   * `apt-get install python3 python3-dateutil python3-stemmer python3-lxml python3-bs4 python3-selenium`

> _**In a case where you dont have the system administrators 
  rights you may use easy install for these plugins
  for example:**_
   * `easy_install3 --user pystemmer`
   * `easy_install3 --user python-dateutil`

--
###**Running the bot**###

> * **Unpack the source code to the destination of your choice**
  1. Modify the `config.py` file to meet your needs
  2. Run the bot with command `./pyBotDaemon.sh` on unix based system (cygwin on windows)
     + Or run `python3 pyBot.py`
     
-- 
###**Something about modules**###


> * Some of the modules (the most of them) are designed to meet our own needs (as we use the bot as well), so in some cases the language might be in finnish. `modules/fmi.py` as in this particular case.
* Cobe plugin is written in `python 2.x` by [Peter Teichman] (https://github.com/pteichman/cobe), but we have modified it to run smoothly also on `python 3.x`

> * Callable modules below:
    * **_`!automodes set <nick> <flag>`_** (current flags are ao/av)
      * **_`!automodes me`_** **_`!automodes reset <nick>`_**
    * **_`!clock`_** current time
    * **_`!conv <amount> <unit>`_** | !conv units
    * **_`!currency <amount> <from> <to>`_**
    * **_`!fap`_** for random porn
    * **_`!fmi set <city>`_** saves preferred city, now you can call **_`!fmi`_** or **_`!fmi <city>`_**
    * **_`!geo <ip/host>`_** tells the physical location of the switch
    * **_`!git`_** lets you pull the latest update from our git branch
    * **_`!google <search term>`_**
      * **_`!google next`_** for the next result
    * **_`!gt <from> <to> <word/sentence>`_** (google translate)
    * **_`!isup <http://domain.com>`_**
    * **_`!op`_**(op for operators)
    * **_`!seen <nick>`_**
    * **_`!stats <nick/word>`_**
    * **_`!sysinfo`_**
    * **_`!tell <nick> <message>`_** (check config for options for this module)
    * **_`!version`_**
    * **_`!wiki <lang> <search term>`_** - e.g. !wiki en finland
      * **_`!wiki next`_** for the next result 
    * **_`!ylilauta`_** random post from ylilauta
    * **_`!youtube <search term>`_**
      * **_`!youtube next`_** for the next result
    * **_`!game`_** to play the slotmachine game  
    
--
###**About the pyBot project**###

> * **All the development is done on Linux and OS X. We don't officially support Windows, but the bot should run just fine :)**
>
* **Feel free to dig in the code, use the bot, write your own modules as you desire or get in touch with us if you want to contribute to this project**
>
* **Now as im writing this, we are about to launch `pyBot version 1.0` and planning to continue the development further forward. Our goal is to improve our skills related to python and over all coding :)**
>
* **We have been working on with this while keeping in our minds that someday this would have a multi chan support. Some of the features are _KINDA_ supporting it, but in the long run it is still far far away from it.**
>
* **So for now the preferred way of using it, _`would be on a single channel`_. Some of the features interracts with each other causing confusion within the bot. But we are looking into that.**
