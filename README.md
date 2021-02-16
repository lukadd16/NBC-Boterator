<!--
Note on how to make documentation suggestions/changes? (would be commented out like this)
-->



<!--
*** CTRL + SHIFT + V to preview
-->



<!-- PROJECT SHIELDS -->
[![Discord][discord-shield]][discord-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Pull Requests][pr-shield]][pr-url]
[![MIT License][license-shield]][license-url]
![GitHub Repository Size][repo-size-shield]
[![Latest Release][release-shield]][release-url]
![Maintenance][maintain-shield]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/lukadd16/NBC-Boterator">
    <img src="data/images/logos/NBC Boterator_Aura.jpg" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">NBC-Boterator</h3>

  <p align="center">
    Custom Bot for the Northbridge Café Discord Server
    <br />
    <br />
    <a href="https://github.com/lukadd16/NBC-Boterator/issues/new/choose">Report a Bug</a>
    ·
    <a href="https://github.com/lukadd16/NBC-Boterator/issues/new/choose">Request a Feature</a>
    ·
    <a href="https://github.com/lukadd16/NBC-Boterator/compare">Open a Pull Request</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents :bookmark_tabs:

* [About the Project](#about-the-project-wave)
  * [Fair Use](#fair-use-bangbang)
  * [Built With](#built-with-hammer_and_wrench)
* [Getting Started](#getting-started-gear)
  * [Prerequisites](#prerequisites-toolbox)
  * [Installation](#installation-computer)
  * [Running](#running-runner)
* [Usage](#usage-mag)
* [Roadmap](#roadmap-construction)
* [Contributing](#contributing-handshake)
* [License](#license-page_facing_up)
* [Contact](#contact-dart)
* [Acknowledgements](#acknowledgements-loudspeaker)



<!-- ABOUT THE PROJECT -->
## About The Project :wave:

This is a simple but tailored discord bot created for the purpose of enhancing user experience within a [tech server][discord-url] that I own (and also because programming is a hobby of mine).

### Fair Use :bangbang:

I don't mind if you run this bot locally and use it in a private discord server with the intention of testing code contributions or learning/experimenting with the discord<span>.py<span> library. In fact, I encourage this (which is why I provide setup instructions below).

What I do not appreciate is anyone who runs a one-to-one copy of this bot with the intention of using it publically, advertising this copy on sites like [top.gg](https://top.gg) and/or claiming it as their own work.

### Built With :hammer_and_wrench:

* [Discord.py](https://pypi.org/project/discord.py/)



<!-- GETTING STARTED -->
## Getting Started :gear:

Here's what you need to do to get a local instance of NBC Boterator up and running:

### Prerequisites :toolbox:

* [Python 3.6+](https://www.python.org/downloads/)
* Git
  * [Windows](https://gitforwindows.org/)
  * [OS X](https://git-scm.com/download/mac)
  * [Linux](https://git-scm.com/download/linux)
* [Discord Application Token](https://discordpy.readthedocs.io/en/latest/discord.html)
<!-- https://git-scm.com/book/en/v2/Getting-Started-Installing-Git -->

### Installation :computer:

1. Open a terminal
2. Switch to the directory that you want the source code to be located in
```sh
cd PATH/TO/YOUR/DIRECTORY
```
3. Clone this repository
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

### Running :runner:

1. Set up the configuration file
* Rename `config.example.py` located in the root directory to `config.py`
<!-- If ever decide to make a proper wiki, create own guide for how to make a discord app & bot account -->
* Populate the `BOT_TOKEN` field with your [discord application token](https://discordpy.readthedocs.io/en/latest/discord.html).
> _:warning:**Note:** Support for fields such as `BOT_EMOJI` or `CHANNEL_ID` will not be provided_
```py
# Discord Application Token
BOT_TOKEN = "your-token-here"

# Bot Prefix
BOT_PREFIX = "jj "

# ...
```
2. Activate the previously created virtual environment
3. Launch the bot
* Windows
```cmd
py main.py
```
* Mac OS/Linux
```sh
python3 main.py
```
4. Success!
> :tada: At this point you should see some output to the terminal telling you that the bot has established a connection to discord.



<!-- USAGE EXAMPLES -->
## Usage :mag:

Run the help command `jj help` for information on how to use each of the bot's commands (minus owner-only commands).

I may add GIFs/screenshots in the future to demonstrate how to use certain commands, who knows ¯\\\_(ツ)_\/¯.



<!-- ROADMAP -->
## Roadmap :construction:

See the [open issues](https://github.com/lukadd16/NBC-Boterator/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
<!--
Add a proper CONTRIBUTING.md file down the line with sections on conduct, issue/PR title format (to match automation), etc.
-->
## Contributing :handshake:

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. [Fork this repository](https://github.com/lukadd16/NBC-Boterator/fork)
2. Clone your Fork (`git clone https://github.com/your-username/NBC-Boterator.git`)
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -am 'Add some AmazingFeature'`) <!--git -am tag stages all tracked, modified files before committing-->
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. [Open a Pull Request](`https://github.com/lukadd16/NBC-Boterator/compare`)



<!-- LICENSE -->
## License :page_facing_up:

Distributed under the BSD 3-Clause License. See [`LICENSE`](https://github.com/lukadd16/NBC-Boterator/blob/master/LICENSE) for more information.



<!-- CONTACT -->
## Contact :dart:

Discord - `Lukadd.16#8870`

Northbridge Café Discord Server (where this bot is solely used) - [Click to join][discord-url] :sunglasses:

Repository Link: [https://github.com/lukadd16/NBC-Boterator](https://github.com/lukadd16/NBC-Boterator)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements :loudspeaker:

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* Discord.py's [amazing documentation](https://discordpy.readthedocs.io/en/latest/)
* Stack Overflow, a programmer's best friend :pray:
* [emoji-cheat-sheet](https://github.com/ikatyang/emoji-cheat-sheet)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

<!-- [discord-shield]: https://img.shields.io/discord/667059292125265941?style=flat-square -->
<!-- [discord-shield]: https://img.shields.io/discord/667059292125265941?color=7289DA&logo=discord&logoColor=ffffff&style=flat-square -->
[discord-shield]: https://discord.com/api/guilds/667059292125265941/widget.png
[discord-url]: https://discord.gg/Wzv2BVQ
[contributors-shield]: https://img.shields.io/github/contributors/lukadd16/NBC-Boterator.svg?style=flat-square
[contributors-url]: https://github.com/lukadd16/NBC-Boterator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/lukadd16/NBC-Boterator.svg?style=flat-square
[forks-url]: https://github.com/lukadd16/NBC-Boterator/network/members
[stars-shield]: https://img.shields.io/github/stars/lukadd16/NBC-Boterator.svg?style=flat-square
[stars-url]: https://github.com/lukadd16/NBC-Boterator/stargazers
[issues-shield]: https://img.shields.io/github/issues/lukadd16/NBC-Boterator.svg?style=flat-square
[issues-url]: https://github.com/lukadd16/NBC-Boterator/issues
[pr-shield]: https://img.shields.io/github/issues-pr/lukadd16/NBC-Boterator?style=flat-square
[pr-url]: https://github.com/lukadd16/NBC-Boterator/pulls
[license-shield]: https://img.shields.io/github/license/lukadd16/NBC-Boterator.svg?style=flat-square
[license-url]: https://github.com/lukadd16/NBC-Boterator/blob/master/LICENSE
[repo-size-shield]: https://img.shields.io/github/repo-size/lukadd16/NBC-Boterator?style=flat-square
<!--[repo-url]: https://github.com/lukadd16/NBC-Boterator-->
[release-shield]: https://img.shields.io/github/v/release/lukadd16/NBC-Boterator?sort=semver&style=flat-square
[release-url]: https://github.com/lukadd16/NBC-Boterator/releases
[maintain-shield]: https://img.shields.io/maintenance/yes/2021?style=flat-square
