# WHU Embergard Card Bot

This is a Discord bot which allows users to quickly load up a preview of Warhammer Underworlds: Embergard cards. 

## Shout-outs

Special thanks to **Mcrat** of [UnderworldsDB](https://underworldsdb.com) for providing the card data and images, as well as all contributors who provide him with the data and card scans ahead of release time.

## Installation

Requires Python 3.9
1. Clone the repository:
    ```bash
    git clone https://github.com/devofdisaster/embergard-card-bot.git
    ```
2. Navigate to the project directory:
    ```bash
    cd embergard-card-bot
    ```
3. Install the required dependencies:
    ```bash
    make install
    ```
4. Create a developer Discord account and set up the application you'll be using for the bot
4. Copy the `.env.dist` file as `.env` and fill in the CLIENT_TOKEN variable with the token for the chosen application

## Usage

1. Run the bot:
    ```bash
    make run
    ```
2. Use the invite link for your application to invite the bot to your Discord server.
3. Done! Go ahead and type `(( card_name_here ))` in your Discord server, and the bot will reply with a list of matching cards or a preview if only one card is found.

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m 'Add new feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature-branch
    ```
5. Create a pull request.

## Forking for modifications
### Card data

The bot uses card data taken directly from [UnderworldsDB](https://underworldsdb.com). Every time a new product comes out, the [local card library](src/resources/library.csv) has to be updated with the new data.
The fighter and warscroll data in [warbands.csv](src/resources/warbands.csv) has to be updated manually, as UnderworldsDB doesn't use such a data sheet.
Additionally, some content has been added to the card descriptions, which needs to be added manually to the data provided by UWDB whenever a new product is released:
- core ability icons (`:core:`)
- surge ability icons (`:surge:`)

### Discord icons

The UWDB data uses a particular set of icons in the card descriptions. Additionally, some additional icons have been added to the card descriptions (like the "core ability" icon).
Since this bot uses a custom set of icons, an icon map has been defined in [replacement_icon_map.py](src/discord/replacement_icon_map.py), and these are used to replace the icons in the card description with proper emojis when rendering a single card message.
If you'd like to use your own set in a forked project, simply replace the values in [custom_icons.py](src/discord/custom_icons.py) with links to icons from any server that your bot has access to. 
To get the specific format used, just type `\:icon_name:` in Discord.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact Veetek#5958 on Discord.
