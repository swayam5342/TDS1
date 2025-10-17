from typing import List
import base64
from app.schema.schema import Data

def process_attachments(attachments: List[Data]) -> str:
    processed_data = []
    for attachment in attachments:
        url = attachment.url
        name = attachment.name
        if url.startswith("data:"):
            try:
                _, encoded_data = url.split(',', 1)
            except ValueError:
                print(f"Error: Invalid data URI format for {name}")
                continue
            try:
                decoded_content = base64.b64decode(encoded_data).decode('utf-8')
                sample_content = decoded_content[:1000] 
                processed_data.append(
                    f"## Attached File: {name}\n"
                    f"--- Content Sample ---\n"
                    f"{sample_content}\n"
                    f"----------------------\n"
                )
            except Exception as e:
                print(f"Error decoding attachment {name}: {e}")
                
    return "\n".join(processed_data)