from anthropic import Anthropic
import streamlit as st
import cv2
from PIL import Image
import base64
import os
from llm.baseagent import BaseClaudeAgent

class HistoryAgent(BaseClaudeAgent):
    
    def analyze(self, history: str):
        
        prompt = f"""You are a clinical reasoning agent that evaluates a patient's health, behavioral, developmental, and social history to identify abnormal features.

                The user will input all historical observations as one unstructured text block.

                Your task is to extract relevant health history features that don't correlate with ideal human features and assess each for clinical relevance.

                Historical Observations: {history}

                For each identified feature, return:

                    "Normal" if it reflects typical development or behavior

                    "Unusual" followed by a specific explanation on how it is abnormal

                    "No Data" if the topic is not mentioned

                Your output must follow this exact format (one item per line):

                    Birth Complications: [Normal / Unusual, explanation / No Data]  
                    Gestational Age: [Normal / Unusual, explanation / No Data]  
                    Family History of Disorders: [Normal / Unusual, explanation / No Data] 
                    Speech Development: [Normal / Unusual, explanation / No Data]  
                    Regression in Speech: [Normal / Unusual, explanation / No Data] 
                    Echolalia (Repeating heard phrases): [Normal / Unusual, explanation / No Data] 
                    Nonverbal Communication: [Normal / Unusual, explanation / No Data] 
                    Eye Contact: [Normal / Unusual, explanation / No Data]  
                    Social Interaction: [Normal / Unusual, explanation / No Data] 
                    Peer Emotion Understanding: [Normal / Unusual, explanation / No Data]  
                    Solitary Preference: [Normal / Unusual, explanation / No Data] 
                    Repetitive Behaviors: [Normal / Unusual, explanation / No Data]  
                    Repetitive Movements: [Normal / Unusual, explanation / No Data] 
                    Sensory Sensitivity: [Normal / Unusual, explanation / No Data] 
                    Intense Focus on Certain Topics: [Normal / Unusual, explanation / No Data] 
                    Trauma History: [Normal / Unusual, explanation / No Data]  
                    Global Development: [Normal / Unusual, explanation / No Data] 
                    Skill Development: [Normal / Unusual, explanation / No Data] 
                    IQ Level: [Normal / Unusual, explanation / No Data] 
                    Academic or Learning Issues: [Normal / Unusual, explanation / No Data]  
                    Mental Illness or Disorder Diagnosis (if any): [Normal / Unusual, explanation / No Data]  
                    Behavioral or Mood Abnormalities: [Normal / Unusual, explanation / No Data]  
                    Sleep Issues: [Normal / Unusual, explanation / No Data] 
                    Seizures or Epilepsy: [Normal / Unusual, explanation / No Data] 
                    Genetic Screening Results: [Normal / Unusual, explanation / No Data] 

                    Additional Mentions: 
                    
                    ...[Normal / Unusual, explanation / No Data] 

                Notes:
                    If observations are mentioned that are not specified in the observation possibilities listed, address each of them under the "Additional Mentions" line."""
        
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