import redis


def connessione():
    redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
    redis_port = 11457
    redis_password = "Password"

    # Connettiti al server Redis
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    return redis_client