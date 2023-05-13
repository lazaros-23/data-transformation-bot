## Load libraries
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain import LLMChain

## Load API key from .env file
from dotenv import dotenv_values
secrets = dotenv_values(".env")
OPENAI_API_KEY = secrets['OPENAI_API_KEY']


## Define template
template = """Given the following product description, output a JSON with the following structure.

Brand Name:"",
Liquor Volume:"",
Pack Size:"",
Category:"",
Flavor:""

Always include all the keys even if the value is empty.

Product Description:
{product}

JSON object:
"""

## Define function
def normalize_text(product_description, template=template):
    """Normalize Product Description into a dict object
    with pre-defined keys.

    Args:
        product_description (str): Product Description

    Returns:
        dict: normalized values of Product Description
    """
    
    # Initialize the OpenAI model
    llm = OpenAI(model_name="text-davinci-003",
             temperature=0.5,
             max_tokens=120,
             openai_api_key=OPENAI_API_KEY)

    # Define the prompt
    prompt = PromptTemplate(template=template,
                            input_variables=["product"])

    # Initialize the LLMChain
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    try:
        answer = llm_chain.run(product_description)
    except:
        answer = "Error: Please enter a valid product description."
    
    return answer