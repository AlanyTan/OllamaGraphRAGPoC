from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    NEO4J_URI: str = "neo4j+s://16cbd7c0.databases.neo4j.io"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "SXt5LodHtuDh-DfLF8VllCBNLLUyc-U_fIoERmQ6eg8"
    AURA_INSTANCEID: str = "16cbd7c0"
    AURA_INSTANCENAME: str ="Insttance01"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_USERNAME: str = ""
    DOC_DIR: str = "input-dir"
    OLLAMA_HOST: str = "localhost"
    OLLAMA_PORT: int = 11434
    OLLAMA_LLM_MODEL: str = "deepseek-r1:14b"
    OLLAMA_EMBED_MODEL: str = "bge-m3"

    @field_validator('NEO4J_USERNAME', 'NEO4J_PASSWORD', 'AURA_INSTANCEID', 'AURA_INSTANCENAME', 
        'REDIS_USERNAME', 'REDIS_PASSWORD', 'OLLAMA_LLM_MODEL', 'OLLAMA_EMBED_MODEL')
    def validate_alphanumeric_and_underscore(cls, v, field):
        if not all(char.isalnum() or char in '_-:.' for char in v):
            raise ValueError(
                f'{field.field_name} must contain only alphanumeric characters and underscores')
        return v

    @field_validator( 'REDIS_HOST',  'OLLAMA_HOST', 'DOC_DIR')
    def validate_name(cls, v, field):
        if not all(char.isalnum() or char in '_.-' for char in v):
            raise ValueError(
                f'{field.field_name} must contain only alphanumeric characters and underscores')
        return v

    @field_validator('REDIS_PORT', 'OLLAMA_PORT')
    def validate_redis_port(cls, value):
        if (not isinstance(value, int)) or (not 0 <= value <= 65535):
            raise ValueError('REDIS_PORT must be between 0 and 65535')
        return value
    
    @field_validator('NEO4J_URI')
    def validate_neo4j_uri(cls, value):
        from urllib.parse import urlparse
        result = urlparse(value)
        if not all([result.scheme, result.netloc]):
            raise ValueError('NEO4J_URI must be a valid URI')
        return value
        

try:
    config = Settings()
except ValidationError as e:
    print(f'Environment variable validation error: {e}')
    config = BaseSettings()
    exit()


def test():
    """
    >>> import os
    >>> os.environ['NEO4J_URI'] = 'neo4j://Valid_URI'
    >>> os.environ['NEO4J_USERNAME'] = 'Valid_Username'
    >>> os.environ['NEO4J_PASSWORD'] = 'Valid_Password'
    >>> os.environ['AURA_INSTANCEID'] = 'Valid_InstanceID'
    >>> os.environ['AURA_INSTANCENAME'] = 'Valid_InstanceName'
    >>> config = Settings()
    >>> config.NEO4J_URI
    'neo4j://Valid_URI'
    >>> config.NEO4J_USERNAME
    'Valid_Username'
    >>> config.NEO4J_PASSWORD
    'Valid_Password'
    >>> config.AURA_INSTANCEID
    'Valid_InstanceID'
    >>> config.AURA_INSTANCENAME
    'Valid_InstanceName'

    """


if __name__ == '__main__':
    import doctest
    doctest.testmod()
