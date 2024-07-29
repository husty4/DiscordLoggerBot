import logging

voice_logger = logging.getLogger('voice_logger')

def log_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        voice_logger.info(f'{member.name} joined voice channel {after.channel.name}')
    elif before.channel is not None and after.channel is None:
        voice_logger.info(f'{member.name} left voice channel {before.channel.name}')
