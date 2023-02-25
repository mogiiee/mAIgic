import os
import openai


openai.api_key = "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"

Role = "Software Engineer"
Organisation = "Mircosoft"
Stipend = "100k $"
Qulification = "B Tech" 
Contact = "achethanreddy1921@gmail.com"

prompt = f"write a job description that highlights the responsibilities and requirements of the {Role}, as well as the benefits of working at the {Organisation}. Make sure to include the {Stipend}, necessary {Qulification}, and {Contact} information for interested applicants. Your job description should be clear, concise, and engaging, and should attract top talent to your organization."

response = openai.Completion.create(
  model="ada",
  prompt=prompt,
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

print(response)