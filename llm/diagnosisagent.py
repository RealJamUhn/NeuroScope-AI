from llm.baseagent import BaseClaudeAgent
from utils.DSM5MCP import DSM5MCPServer

class DiagnosisAgent(BaseClaudeAgent):

    def analyze(self, age, history_analysis, video_analysis, audio_analysis, mcp_context):

        prompt = f"""You are a clinical reasoning agent that uses given evaluations from 3 other Agents to determine how likely it is for this patient to have Autism Spectrum Disorders.

                Your task is to compare the information inputted by the agents with the DSM-5 MCP and determine the likelihood of the patient having ASD, if it is likely that they have ASD, which disorder/s might they have, as well as comorbities.
                
                Also base your conclusion the features of ASD which are found common or not at the patient's age.

                Support your conlcusion with a thorough explanation using commonalities between patient and database features as well as background evidence (Cite DSM-5 and outside sources).

                Patient Data:

                    Age: {age}

                    Medical History and Behavior: {history_analysis}

                    Visual Behavior: {video_analysis}

                    Audible Features: {audio_analysis}

                DSM-5 MCP:

                    {mcp_context}
                
                Your output must follow this exact format (Do not address yourself as an agent. Begin with the first line below):

                    (Nothing before this) It is... (likelihood) that you have an Autism Spectrum Disorder. (If the likelihood is on the likelier side) Specifically ...

                    Possible comorbidities include: (comorbidity): (likelihood)...

                    This is because...
        
                    References: 
                    
                    ..."""
        
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
