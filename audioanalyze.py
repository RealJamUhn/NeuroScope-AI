from llm.baseagent import BaseClaudeAgent
from utils.audio_utils import extract_audio, get_timestamped_transcript, transcript_structure

class AudioAgent(BaseClaudeAgent):

    def analyze(self, transcript):

        prompt = f"""You are a clinical analysis agent that evaluates a given transcript from a video of a patient conversating to identify unusual speech behaviors. 

                Your task is to identify unusual or abnormal speech of the patient that indicate non-ideal human behavior.
                
                The transcript will be inputted and already structured as repetitions of: A question from an interviewer ". " The patient's response time ". " The patient's answer.

                Assume all question sentences are from the interviewer only if they dont seem like an answer (e.g. "Coffee?" - Patient, "How long will..." - Interviewer).

                Transcript: {transcript}

                For each identified feature, return:

                    "Normal" if it reflects typical behavior

                    "Unusual" followed by a specific explanation on how it is abnormal

                    "No Data" if the behavior is not displayed

                Your output must follow this exact format (one item per line):

                    Delayed Answers: [Normal / Unusual, explanation / No Data] 
                    Limited Vocabulary: [Normal / Unusual, explanation / No Data] 
                    Echolalia (Repeating heard phrases): [Normal / Unusual, explanation / No Data] 
                    Repeating Phrases without Understanding: [Normal / Unusual, explanation / No Data] 
                    Frequent Jargon Use: [Normal / Unusual, explanation / No Data] 
                    Use of Made-Up words: [Normal / Unusual, explanation / No Data] 
                    Interepreting Figuratives Literally: [Normal / Unusual, explanation / No Data] 
                    Topic Maintenence: [Normal / Unusual, explanation / No Data] 
                    Trouble Answering Questions: [Normal / Unusual, explanation / No Data] 
                    Innapropriate Response: [Normal / Unusual, explanation / No Data] 
                    No Response: [Normal / Unusual, explanation / No Data] 
                    No Expressive Language: [Normal / Unusual, explanation / No Data] 
                    Word Choice: [Normal / Unusual, explanation / No Data] 
                    Sentence Structure: [Normal / Unusual, explanation / No Data] 

                    Additional Mentions: 
                    
                    ...[Normal / Unusual, explanation / No Data] 

                Notes:
                    If behaviors are displayed that are not specified in the format above, address each of them under the "Additional Mentions" line."""
        
        message_content = [{"type": "text", "text": prompt}]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": message_content
            }]
        )

        return response.content[0].text