from llm.baseagent import BaseClaudeAgent
from utils.image_utils import get_encoded_frames, extract_frames

class VisionAgent(BaseClaudeAgent):
    
    def analyze(self, video_path):
        
        output_path = "C:\\Users\\1094828\\SCSP Hackathon\\frames"
        raw_images = extract_frames(video_path, output_path)
        images = get_encoded_frames(output_path)

        prompt = f"""You are a clinical analysis agent that evaluates given frames sampled from a video of a patient conversating to identify unusual behaviors. 
        
                Your task is to identify unusual or abnormal behaviors of the patient that indicate non-ideal human behavior.
                
                Also compare the frames with each other to identify change of behaviors and expressions. 

                The patient will always be on the right-hand side of the video.

                For each identified feature, return:

                    "Normal" if it reflects typical behavior

                    "Unusual" followed by a specific explanation on how it is abnormal

                    "No Data" if the behavior is not displayed

                Your output must follow this exact format (one item per line):

                    Nonverbal Communication: [Normal / Unusual, explanation / No Data] 
                    Eye Contact: [Normal / Unusual, explanation / No Data]  
                    Visual Peer Emotion Understanding: [Normal / Unusual, explanation / No Data]  
                    Repetitive Movements: [Normal / Unusual, explanation / No Data] 
                    Sensory Sensitivity: [Normal / Unusual, explanation / No Data] 
                    Mood: [Normal / Unusual, explanation / No Data]
                    Facial Expression: [Normal / Unusual, explanation / No Data]
                    Body Language: [Normal / Unusual, explanation / No Data]
                    Shyness: [Normal / Unusual, explanation / No Data]
                    Visual Behavior: [Normal / Unusual, explanation / No Data]
                    Change in Behavior: [Normal / Unusual, explanation / No Data]

                    Additional Mentions: 
                    
                    ...[Normal / Unusual, explanation / No Data] 

                Notes:
                    If behaviors are displayed that are not specified in the format above, address each of them under the "Additional Mentions" line."""

        message_content = [{"type": "text", "text": prompt}] + images

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": message_content
            }]
        )

        return response.content[0].text