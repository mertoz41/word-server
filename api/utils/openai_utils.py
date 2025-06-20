def build_openai_prompt(word, locale, translations=None):
    translations = translations or []

    translations_section = ""
    if translations:
        translations_entries = []
        for lang in translations:
            translations_entries.append(f'''
                "{lang}": {{
                  "word": "translated word",
                  "definition": "definition in that language",
                  "sentences": ["sentence 1 in {lang}", "sentence 2 in {lang}", "sentence 3 in {lang}"]
                }}
            '''.strip())
        translations_str = ", ".join(translations_entries)

        translations_section = f""",
  "translations": {{
    {translations_str}
  }}"""

    # Prepare the translations instructions separately to avoid backslash in f-string expression
    translations_instructions = ""
    if translations:
        translations_instructions = (
            "Additionally, translate the word into the following languages: "
            + ", ".join(translations)
            + ".\nFor each translated language, provide:\n"
            "- The translation of the word.\n"
            "- The definition of the word in that language.\n"
            "- Three example sentences in that language."
        )

    prompt = f'''
        Provide the definition of the word "{word}" in {locale}.
        Then, generate 3 sentences where the word is used in {locale}.

        {translations_instructions}

        Format the response in JSON as follows:
        {{
        "definition": "definition of the word in {locale}",
        "sentences": ["sentence 1 in {locale}", "sentence 2 in {locale}", "sentence 3 in {locale}"]{translations_section}
        }}
        '''.strip()

    return prompt
