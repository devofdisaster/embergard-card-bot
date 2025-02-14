# WHU Embergard Card Bot

This is a Discord bot which allows users to quickly load up a preview of Warhammer Underworlds: Embergard cards.

## Versions

- The https://github.com/devofdisaster/embergard-card-bot/tree/main branch supports the latest edition of the Warhammer Underworlds game (Embergard at time of writing).
- The https://github.com/devofdisaster/embergard-card-bot/tree/v1plus branch supports the first edition of the game, including the `v1+` community project, which contains various card rebalances and custom warbands.

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
3. (Optionally) switch to the `release/v1plus` branch if you want to use the `v1+` version.
4. Install the required dependencies:
    ```bash
    make install
    ```
5. Create a developer Discord account and set up the application you'll be using for the bot
6. Copy the `.env.dist` file as `.env` and fill in:

    1. `CLIENT_TOKEN` variable with the token for the chosen application
    2. `IMAGES_URL` variable with the base URL to custom images (like for plot cards)

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

The bot uses card data taken directly from [UnderworldsDB](https://underworldsdb.com), then trimmed of the unnecessary data. 

Every time a new product comes out, the [local card library](src/resources/library.csv) has to be updated with the new data.

The fighter and warscroll data in [warbands.csv](src/resources/warbands.csv) has to be updated manually, as UnderworldsDB doesn't use such a data sheet.
Additionally, some content has been added to the card descriptions, which needs to be added manually to the data provided by UWDB whenever a new product is released:
- core ability icons (`:core:`)
- surge ability icons (`:surge:`)

#### v1+

The bot uses card data taken directly from [UnderworldsDB](https://underworldsdb.com), trimmed of the unnecessary data, with custom `v1+` changes added in.

Every time an update is made, the [local card library](src/resources/library.csv) has to be updated with the new data.

The fighter data in [warbands.csv](src/resources/warbands.csv) has to be updated manually, as UnderworldsDB doesn't use such a data sheet.

### Custom images

In some cases (like plot cards, or the `v1+` project) you might want to provide custom images for cards, either because you want to bypass UnderworldsDB or because the particular image is not available there. 

To do so, fill in the `IMAGES_URL` environment variable in your `.env` file, as well as the `CustomImage` column in the [library.csv](src/resources/warbands.csv) file.

For example:

`.env`:
```.env
IMAGES_URL="https://some.image.hosting.com/some-folder/nested/folder"
```

`library.csv`:
```csv
Set,Number,Name,(...),CustomImage
Embergard,CC0,Countdown to Cataclysm,(...),"/ctc/plot.png"
```

### Discord icons

The UWDB data uses a particular set of icons in the card descriptions. Additionally, some additional icons have been added to the card descriptions (like the "core ability" icon).
Since this bot uses a custom set of icons, an icon map has been defined in [replacement_icon_map.py](src/discord/replacement_icon_map.py), and these are used to replace the icons in the card description with proper emojis when rendering a single card message.
If you'd like to use your own set in a forked project, simply replace the values in [custom_icons.py](src/discord/custom_icons.py) with links to icons from any server that your bot has access to. 
To get the specific format used, just type `\:icon_name:` in Discord.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact Veetek#5958 on Discord.
