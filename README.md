<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the NBC-Boterator and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->

<!--
*** CTRL + SHIFT + V to preview
-->


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Discord][discord-shield]][discord-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/lukadd16/NBC-Boterator">
    <img src="images/NBC Boterator_Aura.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">NBC-Boterator</h3>

  <p align="center">
    Custom Discord Bot for Northbridge Café
    <br />
    <a href="https://github.com/lukadd16/NBC-Boterator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/lukadd16/NBC-Boterator">View Demo</a>
    ·
    <a href="https://github.com/lukadd16/NBC-Boterator/issues">Report a Bug</a>
    ·
    <a href="https://github.com/lukadd16/NBC-Boterator/issues">Request a Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running](#running)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This is a simple discord bot created for the purpose of XX (talk about tailored/custom commands, more control, etc.)

### !!Please read if you are thinking of cloning this repo!!

I don't mind if you run this bot locally and use it in a private server for the purpose of learning and experimenting with the discord.py library.  What I do not appreciate is if you are running this bot XXX.

### Built With

* [Discord.py](https://pypi.org/project/discord.py/)
  * You can find the documentation for it [here](https://discordpy.readthedocs.io/en/latest/#)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

Git SCM
* [Windows](https://gitforwindows.org/)
* [OS X](https://git-scm.com/download/mac)
* [Linux](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

[Python 3.6 or higher](https://www.python.org/downloads/)

### Installation

1. Open a terminal
2. Change to the directory that you want the repo's source to be located in
```sh
cd PATH/TO/YOUR/DIRECTORY
```
3. Clone the repo
```sh
git clone https://github.com/lukadd16/NBC-Boterator.git
```
4. Create a Python virtual environment (in the current directory)
* Windows
```cmd
py -m venv env
```
* Mac OS/Linux
```sh
python3 -m venv env
```
5. Activate the virtual environment
* Windows
```cmd
.\env\Scripts\activate
```
* Mac OS/Linux
```sh
source env/bin/activate
```
6. Install Dependencies
```sh
pip install -r requirements.txt
```

### Running

1. XX
2. Setup the configuration file
* Create a `config.py` file in the root directory (in relation to where the source is) using the template below.
* Populate the `BOT_TOKEN` field with your discord application token
> _**Note:** Support for fields such as `BOT_EMOJI` or `CHANNEL_ID` will not be provided, XXX._
```py
# Bot Token
BOT_TOKEN = ""

# Bot Prefix
BOT_PREFIX = "jj "

# Initial Extensions
BOT_EXTENSIONS = [
    "cogs.help",
    "cogs.newhelp",
    "cogs.owner",
    "cogs.utilities",
    "cogs.status_loop",
    "cogs.error_handler",
    "cogs.moderation",
    "cogs.fun"
]

# Emojis used throughout the bot
BOT_EMOJI_ARROW = "<:member_join:674374208251232325>"
BOT_EMOJI_BTAG = "<:bot_tag:674379570769821713>"
BOT_EMOJI_ONLINE = "<:status_online:674384199809105933>"
BOT_EMOJI_IDLE = "<:status_idle:674384199448395788>"
BOT_EMOJI_DND = "<:status_dnd:674384199272103946>"
BOT_EMOJI_OFFLINE = "<:status_offline:674384202539728926>"
BOT_EMOJI_STREAM = "<:status_streaming:674384199729414164>"

# Embed Constants
BOT_VERSION = "V1.0.0"
BOT_FEATURES = "Initial Release"
BOT_URL = "http://northbridgecafe.tk"
BOT_AUTHOR_NAME = "NBC Boterator"
BOT_AUTHOR_CLICK = "Click to visit our website!"
BOT_OLDFOOTER = "This bot was created by @Lukadd.16#8870, please DM him if you have any bugs or issues to report."
BOT_FOOTER = f"Found a bug/have an idea? Send it to the dev with {BOT_PREFIX}suggest"
BOT_HELP_USER_ARG = "```Argument is optional but if specified must be a: @mention, userID, or username#discriminator```"
BOT_HELP_REASON_ARG = "```Optional reason argument is a message that will be appended in the server audit log for other moderators to see, if none is provided, a default one will be used.```"
BOT_HELP_BAN_ARG = "```Optional days argument is how many days prior (to a max of 7) that the bot will delete messages sent by the specified user.```"

# Embed Colours
BOT_COLOUR = 0x1cc2ff
BOT_ERR_COLOUR = 0xd80000
BOT_SUCCESS_COLOUR = 0x00e600

LOG_LEVEL = "info"

# Home Server
HOME_SERVER_ID = 667059292125265941

# Status Channel (successful login, successful shutdown, etc.)
STATUS_CHANNEL_ID = 739908797702865126

# Event Logging Channel (joined new server, critical errors, etc.)
EVENTS_CHANNEL_ID = 739908825662095460  # Deprecate?

# Suggestion Channel
SUGGEST_CHANNEL_ID = 739908857094078625
```
3. (talk about activating virtual environment)
4. Launch the bot (reword?)
* Windows
```cmd
py main.py
```
* Mac OS/Linux
```sh
python3 main.py
```
5. Success!



<!-- USAGE EXAMPLES -->
## Usage

Run the help command to learn how to use all of this bot's commands (minus bot owner commands).

I may add GIFs/screenshots in the future to demonstrate how to use certain commands, who knows ¯\\\_(ツ)_\/¯



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/lukadd16/NBC-Boterator/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the BSD 3-Clause License. See `LICENSE` (add link to actual file when it is uploaded) for more information.



<!-- CONTACT -->
## Contact

Discord - `Lukadd.16#8870`

My Discord Tech Server (where this bot is solely used) - [Click To Join](https://discord.gg/Wzv2BVQ)

Repo Link: [https://github.com/lukadd16/NBC-Boterator](https://github.com/lukadd16/NBC-Boterator)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* []()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/lukadd16/NBC-Boterator.svg?style=flat-square
[contributors-url]: https://github.com/lukadd16/NBC-Boterator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/lukadd16/NBC-Boterator.svg?style=flat-square
[forks-url]: https://github.com/lukadd16/NBC-Boterator/network/members
[stars-shield]: https://img.shields.io/github/stars/lukadd16/NBC-Boterator.svg?style=flat-square
[stars-url]: https://github.com/lukadd16/NBC-Boterator/stargazers
[issues-shield]: https://img.shields.io/github/issues/lukadd16/NBC-Boterator.svg?style=flat-square
[issues-url]: https://github.com/lukadd16/NBC-Boterator/issues
[license-shield]: https://img.shields.io/github/license/lukadd16/NBC-Boterator.svg?style=flat-square
[license-url]: https://github.com/lukadd16/NBC-Boterator/blob/master/LICENSE.txt
<!-- [discord-shield]: https://img.shields.io/discord/667059292125265941?style=flat-square -->

[discord-shield]: https://img.shields.io/discord/667059292125265941?color=7289DA&logo=discord&logoColor=ffffff&style=flat-square
[discord-url]: https://discord.gg/Wzv2BVQ
[product-screenshot]: images/screenshot.png
