import logging

message_logger = logging.getLogger('message_logger')

def log_message(message):
    message_logger.info(f'[{message.channel.name}] {message.author.name}: {message.content}')

def log_message_delete(message):
    message_logger.info(f'[{message.channel.name}] {message.author.name}: {message.content} [deleted]')