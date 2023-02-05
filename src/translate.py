import json
import decimalencoder
import todoList
import boto3

def translate_text(text, target_language):
    translate = boto3.client("trasnlate")
    
    response = translate.translate_text(Text=text, TargetLanguageCode=target_language)
    return response["TranslatedText"]

def get(event, context):
    # create a response
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        target_language = event.get("pathParameters", {}).get("target_language", None)
        print(target_language)
        if target_language:
            if target_language == "fr":
                target_language = "fr-FR"
            elif target_language == "it":
                target_language = "it-IT"
            else:
                return {"error": "Unsupported target language"}
              
            translated_text = translate_text(item["text"], target_language)
            item["text"] = translated_text
              
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
