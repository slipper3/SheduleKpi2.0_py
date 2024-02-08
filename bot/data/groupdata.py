# --- File is responsible for saving university group for each telegram group ---
import psycopg2
from bot.data.kapcha import kapcha
# --- Load database config ---
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
dbname = os.getenv("DB_NAME")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
port = os.getenv("PORT")

# --- Save group data ---
async def db_save_group(chatid, groupname):
    """Gets value of `chatid` - id of chat that will be linked with group
    and `groupname` - name of that group, the same as specified on the site\n
    Save chatid and groupname to database"""

    # Check sql request
    if await kapcha(groupname, "groupName") == False:
        return False
    if await kapcha(chatid, "chatID") == False:
        return False
    
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO public.telegram(chatid, groupname) VALUES (%s, %s)
                           ON CONFLICT (chatid) DO UPDATE SET groupname = (%s)""",
                           (chatid, groupname, groupname))
        return True
    except Exception as er:
        #log error
        print(er)
        return False
    finally:
        conn.commit()
        conn.close()


# --- Remove group data ---
async def db_remove_group(chatid) -> None:
    """Gets value of `chatid` - id of chat that was linked with group\n
    Delete row in database that contain `chatid`"""

    # Check sql request
    if await kapcha(chatid, "chatID") == False:
        return False

    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        with conn.cursor() as cursor:
            cursor.execute("""DELETE FROM public.telegram WHERE chatid = (%s)""", (chatid))
        return True
    except Exception as er:
        #log error
        print(er)
        return False
    finally:
        conn.commit()
        conn.close()

# --- Get group data ---
async def db_get_group(chatid):
    """Gets value of `chatid` - id of chat that is linked with group\n
    Show `groupname` in row contain `chatid`"""

    # Check sql request
    if await kapcha(chatid, "chatID") == False:
        return False
    
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        with conn.cursor() as cursor:
            cursor.execute("""SELECT groupname FROM public.telegram WHERE chatid = (%s)""", (chatid))
            result = cursor.fetchone()
        return result[0]
    except Exception as er:
        #log error
        print("query error", er)
        return None
    finally:
        conn.commit()
        conn.close()