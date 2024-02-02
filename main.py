from llama_index import download_loader
from llama_index import VectorStoreIndex, StorageContext, load_index_from_storage
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SimpleWebPageReader = download_loader("SimpleWebPageReader")

loader = SimpleWebPageReader()

urls_to_search = [
    'https://www.sba.gov/business-guide/10-steps-start-your-business',
    'https://www.sba.gov/business-guide/plan-your-business/market-research-competitive-analysis',
    'https://www.sba.gov/business-guide/plan-your-business/write-your-business-plan',
    'https://www.sba.gov/business-guide/plan-your-business/calculate-your-startup-costs',
    'https://www.sba.gov/business-guide/plan-your-business/establish-business-credit',
    'https://www.sba.gov/business-guide/plan-your-business/fund-your-business',
    'https://www.sba.gov/business-guide/plan-your-business/buy-existing-business-or-franchise',
    'https://www.sba.gov/business-guide/launch-your-business/pick-your-business-location',
    'https://www.sba.gov/business-guide/launch-your-business/choose-business-structure',
    'https://www.sba.gov/business-guide/launch-your-business/choose-your-business-name',
    'https://www.sba.gov/business-guide/launch-your-business/register-your-business',
    'https://www.sba.gov/business-guide/launch-your-business/get-federal-state-tax-id-numbers',
    'https://www.sba.gov/business-guide/launch-your-business/apply-licenses-permits',
    'https://www.sba.gov/business-guide/launch-your-business/get-business-insurance',
    'https://www.sba.gov/business-guide/manage-your-business/manage-your-finances',
    'https://www.sba.gov/business-guide/manage-your-business/hire-manage-employees',
    'https://www.sba.gov/business-guide/manage-your-business/pay-taxes',
    'https://www.sba.gov/business-guide/manage-your-business/stay-legally-compliant',
    'https://www.sba.gov/business-guide/manage-your-business/buy-assets-equipment',
    'https://www.sba.gov/business-guide/manage-your-business/marketing-sales',
    'https://www.sba.gov/business-guide/manage-your-business/strengthen-your-cybersecurity',
    'https://www.sba.gov/business-guide/manage-your-business/prepare-emergencies',
    'https://www.sba.gov/business-guide/manage-your-business/recover-disasters',
    'https://www.sba.gov/business-guide/manage-your-business/close-or-sell-your-business',
    'https://www.sba.gov/business-guide/manage-your-business/hire-employees-disabilities',
    'https://www.sba.gov/business-guide/grow-your-business/get-more-funding',
    'https://www.sba.gov/business-guide/grow-your-business/expand-new-locations',
    'https://www.sba.gov/business-guide/grow-your-business/merge-acquire-businesses',
    'https://www.sba.gov/business-guide/grow-your-business/become-federal-contractor',
    'https://www.sba.gov/business-guide/grow-your-business/export-products',
    'https://www.sba.gov/business-guide/grow-your-business/women-owned-businesses',
    'https://www.sba.gov/business-guide/grow-your-business/native-american-owned-businesses',
    'https://www.sba.gov/business-guide/grow-your-business/veteran-owned-businesses',
    'https://www.sba.gov/business-guide/grow-your-business/lgbtq-owned-businesses',
    'https://www.sba.gov/business-guide/grow-your-business/rural-businesses',
    'https://www.sba.gov/business-guide/grow-your-business/minority-owned-businesses'
]

try:
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    # load index
    loadedIndex = load_index_from_storage(storage_context)
except:
    print("Info: No existing index")

def MenuOptions():
    returnString = "\nSelect an action:\n\n"

    options = {
        "L": "Load URLS",
        "G": "Generate Response",
        "C": "Close Program (or CTRL + C)"
    }

    for key in options:
        returnString = returnString + key + ") " + options[key] + "\n"
    
    return returnString

def MenuLogic():
    initialAction = str.lower(input(MenuOptions() + "\nYour Choice: "))

    if initialAction == "l":
        LoadUrls()

    elif initialAction == "g":
        try:
            while True:
                StartChat()
        except KeyboardInterrupt:
            print("\n\nExiting chat!")

    elif initialAction == "c":
        exit()

def LoadUrls():
    global loadedIndex
    documents = loader.load_data(urls_to_search)
    tempIndex = VectorStoreIndex.from_documents(documents)
    tempIndex.storage_context.persist(persist_dir="./storage")
    loadedIndex = tempIndex

def StartChat():
    user_question = input("What is your question?")
    query_engine = loadedIndex.as_query_engine()
    ai_response = query_engine.query(user_question)
    print(ai_response)

def main():
    try:
        while True:
            MenuLogic()
    except KeyboardInterrupt:
        print("\n\nClosing Program!")


if __name__ == '__main__':
    main()