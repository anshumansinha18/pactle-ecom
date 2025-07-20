
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config.env import get_current_env_value


SLACK_TOKEN = get_current_env_value("SLACK_BOT_TOKEN")
CHANNEL_ID = get_current_env_value("SLACK_CHANNEL_ID")

client = WebClient(token=SLACK_TOKEN)

def send_order_notification(user, order, total_amount):
    """
    Sends a formatted Slack message when a new order is placed.
    """
    message = (
        f"New Order Received\n"
        f"UserName: {user.username}\n"
        f"OrderId: {order.id}\n"
        f"Total: Rs.{total_amount}\n"
    )

    try:
        response = client.chat_postMessage(
            channel=CHANNEL_ID,
            text=message
        )
        return response

    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")
        return None
