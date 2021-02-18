# Changelog

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
