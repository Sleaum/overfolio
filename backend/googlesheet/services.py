import os
import gspread
from typing import List
from django.conf import settings
 
def initialize_gspread() -> gspread.client.Client:
    """
    Initialize a gspread client with the given credentials.
    """
    print("🔍 initialize_gspread() called")

    try:
        print("🔍 Getting credentials...")
        credentials = get_credentials()
        print(f"🔍 Credentials type: {type(credentials)}")

        # Vérifier les champs requis
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if not credentials.get(field)]

        if missing_fields:
            print(f"🚨 Missing credential fields: {missing_fields}")
            raise ValueError(f"Missing required credential fields: {missing_fields}")

        print("🔍 Creating gspread client...")
        client = gspread.service_account_from_dict(credentials)
        print(f"🔍 Client created: {type(client)}")

        return client

    except Exception as e:
        print(f"🚨 Exception in initialize_gspread: {e}")
        print(f"🚨 Exception type: {type(e)}")

        # Vérifier si c'est un objet Response
        if hasattr(e, 'status_code'):
            print(f"🚨 FOUND IT! initialize_gspread exception has status_code: {e.status_code}")

        raise
#def initialize_gspread() -> gspread.client.Client:
#  """
#  Initialize a gspread client with the given credentials.
#  """
#  return gspread.service_account_from_dict(get_credentials())  # Note: we could move this to settings to do this once.
 
def get_credentials() -> dict:
  """
  Return gspread credentials.
  """
  return {
          "type": os.getenv("TYPE"),
          "project_id": os.getenv("PROJECT_ID"),
          "private_key_id": os.getenv("PRIVATE_KEY_ID"),
          "private_key": os.getenv("PRIVATE_KEY"),
          "client_email": os.getenv("CLIENT_EMAIL"),
          "client_id": os.getenv("CLIENT_ID"),
          "auth_uri": os.getenv("AUTH_URI"),
          "token_uri": os.getenv("TOKEN_URI"),
          "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
          "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
          "universe_domain": os.getenv("UNIVERSE_DOMAIN")
  }


def get_all_rows(doc_name: str, sheet_name: str = None) -> List[dict]:
    """
    Fetches all rows from a given Google Sheet worksheet.
    """
    print(f"🔍 get_all_rows called with doc_name={doc_name}, sheet_name={sheet_name}")
    
    try:
        # Vérifier que le client est initialisé
        print("🔍 Step 1: Checking GSPREAD_CLIENT...")
        if not hasattr(settings, 'GSPREAD_CLIENT'):
            print("🚨 settings has no GSPREAD_CLIENT attribute")
            raise ValueError("GSPREAD_CLIENT attribute not found")
        
        if settings.GSPREAD_CLIENT is None:
            print("🚨 GSPREAD_CLIENT is None")
            raise ValueError("GSPREAD_CLIENT is None")
        
        print(f"🔍 GSPREAD_CLIENT type: {type(settings.GSPREAD_CLIENT)}")
        
        # Ouvrir le document Google Sheets
        print("🔍 Step 2: Opening document...")
        try:
            sh = settings.GSPREAD_CLIENT.open(doc_name)
            print(f"🔍 Document opened successfully: {type(sh)}")
        except Exception as e:
            print(f"🚨 Error opening document: {e}")
            print(f"🚨 Error type: {type(e)}")
            raise
        
        # Sélectionner la worksheet
        print("🔍 Step 3: Selecting worksheet...")
        try:
            if sheet_name:
                print(f"🔍 Getting worksheet by name: {sheet_name}")
                worksheet = sh.worksheet(sheet_name)
            else:
                print("🔍 Getting first worksheet (index 0)")
                worksheet = sh.get_worksheet(0)
            print(f"🔍 Worksheet selected: {type(worksheet)}")
        except Exception as e:
            print(f"🚨 Error selecting worksheet: {e}")
            print(f"🚨 Error type: {type(e)}")
            raise
        
        # Récupérer toutes les données
        print("🔍 Step 4: Getting all records...")
        try:
            records = worksheet.get_all_records()
            print(f"🔍 Records retrieved successfully")
            print(f"🔍 Records type: {type(records)}")
            print(f"🔍 Records length: {len(records) if isinstance(records, (list, tuple)) else 'Not a list/tuple'}")
            
            # Vérifier si records est vraiment une liste
            if isinstance(records, list):
                print(f"🔍 First record preview: {records[0] if records else 'Empty list'}")
            else:
                print(f"🚨 WARNING: records is not a list! Content: {str(records)[:100]}")
            
            return records
            
        except Exception as e:
            print(f"🚨 Error getting records: {e}")
            print(f"🚨 Error type: {type(e)}")
            raise
        
    except gspread.SpreadsheetNotFound as e:
        print(f"🚨 SpreadsheetNotFound: {e}")
        raise ValueError(f"Google Sheet '{doc_name}' not found or not accessible")
    except gspread.WorksheetNotFound as e:
        print(f"🚨 WorksheetNotFound: {e}")
        raise ValueError(f"Worksheet '{sheet_name}' not found in '{doc_name}'")
    except gspread.exceptions.APIError as e:
        print(f"🚨 APIError: {e}")
        raise ValueError(f"Google Sheets API error: {str(e)}")
    except Exception as e:
        print(f"🚨 Generic Exception in get_all_rows: {e}")
        print(f"🚨 Exception type: {type(e)}")
        print(f"🚨 Exception repr: {repr(e)}")
        
        # Vérifier si l'exception elle-même est un objet Response
        if hasattr(e, 'status_code'):
            print(f"🚨 FOUND IT! Exception has status_code: {e.status_code}")
        
        raise ValueError(f"Failed to access Google Sheet: {str(e)}")



  #def get_all_rows(doc_name: str, sheet_name: str = None) -> List[dict]:
  #  """
  #  Fetches all rows from a given Google Sheet worksheet.
  #  """
  #  sh = settings.GSPREAD_CLIENT.open(doc_name)
  #  worksheet = sh.worksheet[sheet_name] if sheet_name else sh.get_worksheet(0)
  #  return worksheet.get_all_records()

#def get_all_rows(doc_name: str, sheet_name: str = None) -> List[dict]:
#    """
#    Fetches all rows from a given Google Sheet worksheet.
#    """
#    try:
#        # Vérifier que le client est initialisé
#        if not hasattr(settings, 'GSPREAD_CLIENT') or settings.GSPREAD_CLIENT is None:
#            raise ValueError("GSPREAD_CLIENT not initialized in settings")
#        
#        # Ouvrir le document Google Sheets
#        sh = settings.GSPREAD_CLIENT.open(doc_name)
#        
#        # CORRECTION CRITIQUE: Utiliser () au lieu de []
#        worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
#        
#        # Récupérer toutes les données
#        return worksheet.get_all_records()
#        
#    except gspread.SpreadsheetNotFound:
#        raise ValueError(f"Google Sheet '{doc_name}' not found or not accessible")
#    except gspread.WorksheetNotFound:
#        raise ValueError(f"Worksheet '{sheet_name}' not found in '{doc_name}'")
#    except gspread.exceptions.APIError as e:
#        raise ValueError(f"Google Sheets API error: {str(e)}")
#    except Exception as e:
#        raise ValueError(f"Failed to access Google Sheet: {str(e)}")













