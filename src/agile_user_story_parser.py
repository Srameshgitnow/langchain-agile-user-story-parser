from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import getpass
import os
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=os.environ["OPENAI_API_KEY"])

title_schema = ResponseSchema(name="title",
                             description="extract the title if specfically mentioned as 'title'\
                             or make a breif, clear name.")
description_schema = ResponseSchema(name="description",
                             description="define the description if mentioned specifically as 'description'\
                             or make a clear consise explanation of requirment.")
acceptance_criteria_1_schema = ResponseSchema(name="acceptance_criteria_1",
                             description="define the acceptance criteria 1 if mentioned specifically as 'acceptance criteria 1 or AC 1'\
or Make a checklist of condition 1 that must be met for the user story requirment.\
Avoid using comma-separated conditions. Instead, break each condition into its own acceptance criterion, \
starting from acceptance_criteria_2, acceptance_criteria_3, and so on, if there is more than one.")
acceptance_criteria_2_schema = ResponseSchema(name="acceptance_criteria_2",
                             description="define the acceptance criteria 2 if mentioned specifically as 'acceptance criteria 2 or AC 2'\
                             or Make a checklist of condition 2 that must be met for the user story requirment.")
acceptance_criteria_3_schema = ResponseSchema(name="acceptance_criteria_3",
                             description="define the acceptance criteria 3 if mentioned specifically as 'acceptance criteria 3 or AC 3'\
                             or Make a checklist of condition 3 that must be met for the user story requirment.")
acceptance_criteria_4_schema = ResponseSchema(name="acceptance_criteria_4",
                             description="define the acceptance criteria 4 if mentioned specifically as 'acceptance criteria 4 or AC 4'\
                             or Make a checklist of condition 4 that must be met for the user story requirment.")
acceptance_criteria_5_schema = ResponseSchema(name="acceptance_criteria_5",
                             description="define the acceptance criteria 5 if mentioned specifically as 'acceptance criteria 5 or AC 5'\
                             or Make a checklist of condition 5 that must be met for the user story requirment.")
severity_schema = ResponseSchema(name="severity",
                                      description="define the severity if spefically mentioned\
                                      or make it like based on the purpose such as from feature, bug fix, improvment or technical task.")
type_schema = ResponseSchema(name="type",
                                    description="define the type if spefically mentioned\
                                    or make it like based on the purpose such as from feature, bug fix, improvment or technical task.")

response_schemas = [title_schema, 
                    description_schema,
                    acceptance_criteria_1_schema,
                    acceptance_criteria_2_schema,
                    acceptance_criteria_3_schema,
                    acceptance_criteria_4_schema,
                    acceptance_criteria_5_schema,
                    severity_schema,
                    type_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

system_template2 = """\
For the following text, extract the following information to create the user story:

title: extract the title if specfically mentioned as "title" or make a breif, clear name.

description: define the description if mentioned specifically as "description" or make a clear consise explanation of requirment.

acceptance_criteria_1: define the acceptance criteria 1 if mentioned specifically as "acceptance criteria 1 or AC 1"\
or Make a checklist of condition 1 that must be met for the user story requirment.\
Avoid using comma-separated conditions. Instead, make it to new acceptance criteria \
to the instructions accepance_criteria_2, accepance_criteria_3...etc if more than one condition.

acceptance_criteria_2: define the acceptance criteria 2 if mentioned specifically as "acceptance criteria 2 or AC 2"\
or Make a checklist of condition 2 that must be met for the user story requirment.\
leave it as empty if its duplicate

acceptance_criteria_3: define the acceptance criteria 3 if mentioned specifically as "acceptance criteria 3 or AC 3"\
or Make a checklist of condition 3 that must be met for the user story requirment. leave it as empty if its duplicate

acceptance_criteria_4: define the acceptance criteria 4 if mentioned specifically as "acceptance criteria 4 or AC 4"\
or Make a checklist of condition 4 that must be met for the user story requirment. leave it as empty if its duplicate

acceptance_criteria_5: define the acceptance criteria 5  if mentioned specifically as "acceptance criteria 5 or AC 5"\
or Make a checklist of condition 5 that must be met for the user story requirment. leave it as empty if its duplicate

severity : define the severity if spefically mentioned,\
or make it as from how critical the user story is like Low, Medium, High, Critical.

type : define the type if spefically mentioned,\
or make it like based on the purpose such as from feature, bug fix, improvment or technical task.

Format the output as JSON with the following keys:
title
description
acceptance_criteria_1
acceptance_criteria_2
acceptance_criteria_3
acceptance_criteria_4
acceptance_criteria_5
severity
type

text: {text}
"""

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template2), ("user", "{text}")]
)
user_story_requirement = """\
 I want an option to stay logged in, so that i dont have to enter my credentials every time.
"""
prompt = prompt_template.invoke({"text": user_story_requirement})

response = llm.invoke(prompt)

output_dict = output_parser.parse(response.content)
print(output_dict)