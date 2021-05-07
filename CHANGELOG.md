# Changelog

### [1.8.1](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.8.0...v1.8.1) (2021-05-07)


### Bug Fixes

* **disboard:** Ignore AttributeError on first run of check_description ([831f91e](https://www.github.com/lukadd16/NBC-Boterator/commit/831f91e544e337a83516f4c00b167c52f68461e0))

## [1.8.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.7.1...v1.8.0) (2021-05-07)


### Features

* [WIP] Implement custom checks for future use in moderation commands ([1b397d0](https://www.github.com/lukadd16/NBC-Boterator/commit/1b397d00d315de873f3c3fb395b760e198042eca))


### Bug Fixes

* **disboard:** Fetched notif channel from wrong server ([6d7678c](https://www.github.com/lukadd16/NBC-Boterator/commit/6d7678cc4db289a0e859fecc22a8de9396644df4))
* Last automated bump message should be deleted when the server is bumped again ([679e20e](https://www.github.com/lukadd16/NBC-Boterator/commit/679e20ef98e48be1d82a465ac8980c91608e100a))

### [1.7.1](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.7.0...v1.7.1) (2021-04-25)


### Bug Fixes

* **disboard:** Avoid uncaught AttributeError (when description is NoneType) ([3c9b605](https://www.github.com/lukadd16/NBC-Boterator/commit/3c9b605230f02646828195dd879dd2a834d32d5b))
* **disboard:** Use path.join rather than string literals when finding FP to settings.ini ([2f8b4ef](https://www.github.com/lukadd16/NBC-Boterator/commit/2f8b4efad182f0858ff3c2d1c19a7911e228ce2b))

## [1.7.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.6.0...v1.7.0) (2021-04-25)


### Features

* Automated messages when server can be bumped on disboard.org ([#67](https://www.github.com/lukadd16/NBC-Boterator/issues/67)) ([2b13c41](https://www.github.com/lukadd16/NBC-Boterator/commit/2b13c41314a1ffc0c655d49109230f7b07fbb6e6))

## [1.6.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.5.0...v1.6.0) (2021-04-16)


### Features

* Incorporate tools.py delta_datetime functionality into whois command ([3e0b884](https://www.github.com/lukadd16/NBC-Boterator/commit/3e0b8842d01b868eb93170bcc924a743de5e2b19))
* Refactor cog and add new functionality to assist process of updating existing partner records ([#65](https://www.github.com/lukadd16/NBC-Boterator/issues/65)) ([417f0ec](https://www.github.com/lukadd16/NBC-Boterator/commit/417f0ecb9187880d0bff67ff2b6a496902e0621e))
* **utilities:** Add field to whois command that indicates how long ago the specified user last sent a message in the guild ([e6ba8a5](https://www.github.com/lukadd16/NBC-Boterator/commit/e6ba8a586946da39d16eae95d9532c148dc7807f))
* **utilities:** Colour of sidebar in embed response from whois command will match the colour of the specified member's top-most role ([2f13d3e](https://www.github.com/lukadd16/NBC-Boterator/commit/2f13d3e0b2eff904f2b56add4f9a4ee3230e24f5))


### Bug Fixes

* Add local error handler to pinned command to catch 403 Forbidden errors ([897df04](https://www.github.com/lukadd16/NBC-Boterator/commit/897df048cc7c18f92ece4ccab1eb38a406087875))

## [1.5.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.4.3...v1.5.0) (2021-04-05)


### Features

* New Owner-only Help Subcommand; Rename class ([7492340](https://www.github.com/lukadd16/NBC-Boterator/commit/74923404eded8e2ee9477ded7976cf7678165d0e))
* Strip markdown and mentions from pinfo Content field; Add Modified field; Specify how long ago the message was sent/edited ([25dfb7a](https://www.github.com/lukadd16/NBC-Boterator/commit/25dfb7a430eb800a065728895357a7cfa4275129))


### Bug Fixes

* Add +1 to value calculated in get_join_position() helper method ([09eb8a4](https://www.github.com/lukadd16/NBC-Boterator/commit/09eb8a46b441635d1f95076852cc725abd8e8ae7))
* Add helper method that returns how many sec/min/hrs/days ago a datetime object is relative to today; Refactor logic to convert seconds into readable time format ([d272f01](https://www.github.com/lukadd16/NBC-Boterator/commit/d272f016b959169354d825f45b7386ceb64541f5))

### [1.4.3](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.4.2...v1.4.3) (2021-02-18)


### Bug Fixes

* Add missing newlines to separate description links in 'about' command; Fix problematic discord text markdown ([da0f794](https://www.github.com/lukadd16/NBC-Boterator/commit/da0f794d9fea9e2b140f19322de2e1a03ec2bb19))

### [1.4.2](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.4.1...v1.4.2) (2021-02-18)


### Bug Fixes

* Hotfix to address references to outdated config variable names ([c7a0302](https://www.github.com/lukadd16/NBC-Boterator/commit/c7a030243818849c64ec8d48dc0c656cf9825091))

### [1.4.1](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.4.0...v1.4.1) (2021-02-18)


### Bug Fixes

* Remove unused get_channel() call for deprecated events channel functionality ([720dade](https://www.github.com/lukadd16/NBC-Boterator/commit/720dade34043681e7129bd2c9171b03d68cee1cc))

## [1.4.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.3.3...v1.4.0) (2021-02-18)


### Features

* New Partners Cog ([#40](https://www.github.com/lukadd16/NBC-Boterator/issues/40)) ([c29ceba](https://www.github.com/lukadd16/NBC-Boterator/commit/c29ceba7c2e07990c2af8de3b06f018875a8d28d))


### Bug Fixes

* Add two new links in 'about' command description field ([6ce0c90](https://www.github.com/lukadd16/NBC-Boterator/commit/6ce0c902fb4b7e42d48e138200ba49f8fd19399e))

### [1.3.3](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.3.2...v1.3.3) (2021-02-16)


### Bug Fixes

* **owner:** Add confirmation of status cmd completing; No longer need to specify 'cogs.' in cog-related cmds ([e2a10fc](https://www.github.com/lukadd16/NBC-Boterator/commit/e2a10fcbb81342cfbc4e81e425133a4556c36d2d))

### [1.3.2](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.3.1...v1.3.2) (2021-02-11)


### Bug Fixes

* **main:** Fix method call that referenced an outdated method name from tools module ([3f20d26](https://www.github.com/lukadd16/NBC-Boterator/commit/3f20d265269092486fb75464245d043efcff778f))

### [1.3.1](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.3.0...v1.3.1) (2021-02-01)


### Bug Fixes

* **errorhandler:** Fix bug preventing cooldown error msgs from being deleted after cooldown has elapsed ([67f2d78](https://www.github.com/lukadd16/NBC-Boterator/commit/67f2d7867e3376b2ce0cdf5b9aa1517f51b61382))

## [1.3.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.2.0...v1.3.0) (2021-02-01)


### Features

* New 'pinned' command ([#29](https://www.github.com/lukadd16/NBC-Boterator/issues/29)) ([fb70eee](https://www.github.com/lukadd16/NBC-Boterator/commit/fb70eee2bb95f4b6a656959e6af705983a6d1d00))


### Bug Fixes

* **errorhandler:** Cooldown error msgs now auto-delete after the mentioned cooldown has expired ([b226421](https://www.github.com/lukadd16/NBC-Boterator/commit/b2264210e6725fc08a976239c8817417f3ca87c3))
* **owner:** Rename utils subcommand to tools ([38e74d0](https://www.github.com/lukadd16/NBC-Boterator/commit/38e74d008e7147113e8ba34c4e0595e3ecd18383))
* Rename botUtils.py module to tools.py; Correct all references to botUtils in the codebase to point to tools ([5f002bb](https://www.github.com/lukadd16/NBC-Boterator/commit/5f002bb727da1ee94695769c71ff26f88dfcc1c1))
* Replace all references to self.bot.config with config, import config file locally if needed ([d43c938](https://www.github.com/lukadd16/NBC-Boterator/commit/d43c938af3001338710d4ca0a5ab664abcf8aa51))


### Reverts

* **deps:** Revert bumping multidict to 5.1.0 ([a42c998](https://www.github.com/lukadd16/NBC-Boterator/commit/a42c9980bfb3e3b24f4fa1b5194611f58ee82048))

## [1.2.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.1.0...v1.2.0) (2021-01-26)


### Features

* **logging:** Overhaul of application logging ([#10](https://www.github.com/lukadd16/NBC-Boterator/issues/10)) ([fb65ca9](https://www.github.com/lukadd16/NBC-Boterator/commit/fb65ca9cff7dcfb147a8b6d994ab0915f1adba31))

## [1.1.0](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.0.2...v1.1.0) (2021-01-23)


### Features

* **owner:** New 'status' cmd that allows bot owner to send embeds in the status channel ([ec4c30e](https://www.github.com/lukadd16/NBC-Boterator/commit/ec4c30e852ce4ff7f4deb374253d125794a79e10))
* **owner:** Restructure reload cmds using subcmds; rename methods; change owner check to be global to the cog ([f90e4f7](https://www.github.com/lukadd16/NBC-Boterator/commit/f90e4f7c991b1da34b833032fcd68e6bece3b0f6))


### Bug Fixes

* **help:** Add help cmd for joinpos; Remove straggling aliases; Remove mention of reason arg in purge cmd ([ad9fba2](https://www.github.com/lukadd16/NBC-Boterator/commit/ad9fba2a1755d657337cb9f4c10dd5ca4a267ff3))
* **main:** Convert bootup and keyboard interrupt status messages to embeds ([cb627f7](https://www.github.com/lukadd16/NBC-Boterator/commit/cb627f7945a1a0ad9ed2e35c4a0328b20a8653d2))
* **main:** Fix calling await within non-async function ([ed9802c](https://www.github.com/lukadd16/NBC-Boterator/commit/ed9802c1eb616d1109d6794c6817e3aba51fb3de))
* **main:** icon_url is an attribute of app_info not the NBCBoterator class ([f2ddf45](https://www.github.com/lukadd16/NBC-Boterator/commit/f2ddf454dd9d5890e8447ee81a0fe4d692c41091))
* **main:** Use botUtils.py function for calculating uptime in shutdown triggered by keyboard interrupt ([4013369](https://www.github.com/lukadd16/NBC-Boterator/commit/4013369a4271a667cea460e06e2d4421d122a19c))
* **owner:** *sigh* icon_url is invalid, meant to use avatar_url ([8b19202](https://www.github.com/lukadd16/NBC-Boterator/commit/8b1920296e60ea6b28c2293a1a65355df1672bf8))
* **owner:** *sighs again* Forgot to name intended emoji after copy-paste ([106ec33](https://www.github.com/lukadd16/NBC-Boterator/commit/106ec339b3cd26a3aeac40ae8b50bb27aae0c1e5))
* **owner:** Add 'reason' field to shutdown embed ([c160cba](https://www.github.com/lukadd16/NBC-Boterator/commit/c160cba5b7b1664eba98e2597373ca247d8483c7))
* **owner:** Convert status channel response for shutdowns to embed ([0dcbdbc](https://www.github.com/lukadd16/NBC-Boterator/commit/0dcbdbcb79cfaf0ee08643624bb9fb2edb207fb2))
* **owner:** Fix stupid mistakes with subcmd decorators; Move cog logic within creload to its own subcmd ([bc967b0](https://www.github.com/lukadd16/NBC-Boterator/commit/bc967b0b2356d1533fdd505531b79314293e091a))
* **owner:** icon_url is an attribute of user not bot ([8c2965c](https://www.github.com/lukadd16/NBC-Boterator/commit/8c2965c246284fad0463a215bc69c2f9e6d66766))

### [1.0.2](https://www.github.com/lukadd16/NBC-Boterator/compare/v1.0.1...v1.0.2) (2021-01-16)


### Bug Fixes

* **errorhandler:** Remove unnecessary newlines in missing permissions error response ([f6d09f4](https://www.github.com/lukadd16/NBC-Boterator/commit/f6d09f4547249f0ad13652b8f8e15b412dd472fc))
* **help:** Add entry for purge cmd; Remove aliases from help subcommands; Add mention of joinpos cmd (pending own subcommand); Convert single-quotes to double-quotes ([48a96a2](https://www.github.com/lukadd16/NBC-Boterator/commit/48a96a27fc92603854cc820e9819e57ca44d1a60))
* **utilities:** Add short blurb above stats + links to server socials; Remove commented out code ([1b0cea3](https://www.github.com/lukadd16/NBC-Boterator/commit/1b0cea3cfa083cd84b1cbe75ce614a7ad0c5af3b))
* **utilities:** Forgot newline on website line ([716fb6e](https://www.github.com/lukadd16/NBC-Boterator/commit/716fb6e6c3d72828df1235f8a5915125c749a51d))
* **utilities:** Make keyword member arg to be without unlimited positional args; Prep work for new version cmd functionality ([0130439](https://www.github.com/lukadd16/NBC-Boterator/commit/01304392d922a884f6244b7af643378d33ce1f9c))
* **utilities:** Move get_channel to __init__ ([62c9edb](https://www.github.com/lukadd16/NBC-Boterator/commit/62c9edb7692c1af28eb1bc86859c9267b36d9cbe))
* **utilities:** Version num retrieved as proper string; rearrange embed structure ([6418870](https://www.github.com/lukadd16/NBC-Boterator/commit/64188702aca89ddb7e886c5baade297478a6bfab))

### [1.0.1](https://www.github.com/lukadd16/NBC-Boterator/compare/1.0.0...v1.0.1) (2021-01-10)


### Bug Fixes

* **errorhandler:** Adds behaviour to ignore error if originating cog has a local handler, convert if statements to proper elif, minor refactoring ([c2496fc](https://www.github.com/lukadd16/NBC-Boterator/commit/c2496fc960a30a7f877a9b209714391134e0c7c1))
* **main:** Shutdown triggered by KeyboardInterrupt wasn't being reported in status channel ([acd2eb7](https://www.github.com/lukadd16/NBC-Boterator/commit/acd2eb772a2b08aed80a76d85cbe41b154195707))
* **utilities:** Replace double backticks with single ones ([762ee44](https://www.github.com/lukadd16/NBC-Boterator/commit/762ee4484988ca465ba7fdb8ad9fd267e1548e40))
