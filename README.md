# Sysarmy Telegram Bot

This is the Sysarmy Galicia Telegram bot. This bot is designed to manage karma between users, provide event information, split the bill during AdminCañas, and includes some fun interactive options.

## Index

- [Requirements](#requirements)
- [Installation](#installation)
- [Commands](#commands)
- [Contribution](#contribution)

## Requirements

- Python 3.10 or higher
- Dependencies specified in the `pyproject.toml` file

## Installation

1. **Clone the repository to your local machine:**

2. **Install the necessary dependencies using `uv`**: https://docs.astral.sh/uv/getting-started/installation/

   First, install `uv` if you haven’t already:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Then, install the project dependencies with `uv`:

   ```bash
    make install
   ```

   OR

   ```bash
    uv sync --frozen
   ```

3. **Configure the bot with your Telegram token. Create a `.env` file in the root directory and add the following line:**

```bash
BOT_TOKEN=your_token_here
```

4. **Run the bot using `uvicorn`:**

```bash
uv run main.py
```

## Commands

**General Commands:**

- **/start**: Sends a welcome message when a user initiates a conversation with the bot. Used to verify that the bot is functioning.

- **/beer**: Provides information about the next "AdminCañas" event, our monthly social gathering (First Friday of each month 😉).

- **/pineapple**: Sends a fun message about pineapple, considered a tropical delicacy by some.

- **/help**: Displays a list of all enabled commands in the bot, providing a quick guide for users.

- **/holidays**: Informs about the next holiday in Galicia. This command accepts an optional parameter (str) to indicate a specific department and get details about regional holidays.

```bash
/holidays Arteixo
```

**Karma Commands:**

- **/kup [user]**: Increases the karma of a user or thing by one. Ideal for recognizing good actions or comments.

```bash
/kup @Qrow01
```

- **/kdown [user]**: Decreases the karma of a user or thing by one. Used to mark inappropriate behavior or comments.

```bash
/kdown Java
```

- **/kshow [user]**: Displays the current karma level of a specific user or thing.

```bash
/kshow @Qrow01
```

- **/klist**: Shows a ranking of users and things with the most and least karma, allowing you to see who is most (or least) appreciated in the group.

**Menu Commands:**

(These commands are only enabled for the 'Food Orders' channel, which remains closed until the day of AdminCañas. If you want to adapt this bot for your own purposes, modify the `FOOD_THREAD_ID` in `dinner.py` with your own thread ID.)

(Administrators must start the dinner for these commands to be enabled.)

- **/order [id_number]**: Allows users to order a menu item based on a provided identification number. An additional number (int) can be provided as a second argument to order more than one item.

```bash
/order 23 2
```

- **/beer**: Adds a beer to the account of the user sending the command. This command is useful for splitting the bill at the end of an event, thanks to the idea of @jjqrs.

## Contribution

Contributions are welcome. If you want to improve this project, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a Pull Request.
