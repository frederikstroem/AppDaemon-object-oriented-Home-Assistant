# AppDaemon [Python] object oriented [OOP] Home Assistant
This is a snapshot [2023-06-15] of some of my work on an AppDaemon [Python] object-oriented (OOP) Home Assistant setup. I've also set up simple continuous deployment (CD) ⚙️ using a hacky Git 🐙, Rust 🦀 Actix-web backend, and webhooks 🎣 for this part. This seems necessary because AppDaemon's hot reload appears to be broken when running this type of OOP setup, requiring a complete restart of AppDaemon. 🫠

Feel free to *use*, *copy*, *modify*, *share* and *train* upon this code however you like.

## Setup
- **Step 01:**<br>
Clone this repo into to the config dir `/config/`.
- **Step 02:**<br>
Add a Git pull shell command to `/config/configuration.yaml`.<br>
```yaml
shell_command:
    pull_appdaemon: cd /config/appdaemon && git pull
```

See also [Naming scheme](NAMING_SCHEME.md).

## Litterature
### General
- [Community Tutorials](https://appdaemon.readthedocs.io/en/latest/COMMUNITY_TUTORIALS.html)
- [Example apps](https://github.com/AppDaemon/appdaemon/tree/dev/conf/example_apps)
- [Helper Classes](https://community.home-assistant.io/t/creating-help-classes/300809)

### API references
- [HASS API Reference](https://appdaemon.readthedocs.io/en/latest/HASS_API_REFERENCE.html)
- [AppDaemon API Reference](https://appdaemon.readthedocs.io/en/latest/AD_API_REFERENCE.html)
- [AppDaemon Tutorial for HASS Users](https://appdaemon.readthedocs.io/en/latest/HASS_TUTORIAL.html)
