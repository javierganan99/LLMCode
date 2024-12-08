# Reference for `llmcode/utils/logger.py`

This module configures logging for the application, ensuring compatibility across platforms.

It sets up a logging configuration with platform-specific adjustments, such as filtering
out emojis on Windows systems to prevent display issues.

Functions:
    set_logging: Configures the logging settings for the application.
    emojis: Returns an emoji-safe version of a string based on the platform.

Classes:
    EmojiFilter: A custom logging filter class for removing emojis in log messages.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE

<br>

## ::: llmcode.utils.logger.EmojiFilter

<br><br><hr><br>

## ::: llmcode.utils.logger.set_logging

<br><br><hr><br>

## ::: llmcode.utils.logger.emojis

<br><br>
