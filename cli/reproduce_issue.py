from promptmasker import PromptMasker
try:
    masker = PromptMasker()
    query = "my secret is ghjkabygfweiohfijsknejkgbjksejfj"
    result = masker.mask(query)
    print(f"Type: {type(result)}")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
