"""
Class for managing language models and dataframes associated with user sessions.
"""
from datetime import datetime
class AgentObj:
    """
    Class representing an agent.

    This class provides methods to add, get, and disconnect agents.
    """

    agent = {}

    @classmethod
    def add_agent(cls, user_id, model_name):
        """
        Add an agent to the class variable.

        Args:
            user_id (str): ID of the user
            model_name (str): Name of the model
        """
        cls.agent[user_id] = model_name

    @classmethod
    def get_agent(cls, session_id):
        """
        Get agent information for a given session ID.

        Args:
            session_id (str): Unique identifier for the session.

        Returns:
            list: List containing agent information.
        """
        return cls.agent[session_id]

    @classmethod
    def disconnect_agent(cls, session_id):
        """
        Disconnect an agent for a given session ID.

        Args:
            session_id (str): Unique identifier for the session.
        """
        if session_id in cls.agent:
            del cls.agent[session_id]
    @classmethod
    def periodic_disconnect_agent(cls):
        """
        Disconnect an agent for a given session ID.

        Args:
            session_id (str): Unique identifier for the session.
        """
        temp = cls.agent.copy()
        for session_id in list(temp.keys()):
            if (datetime.now()-temp[session_id]["time"]).total_seconds() / 60 >= 60:
                del temp[session_id]
        cls.agent=temp