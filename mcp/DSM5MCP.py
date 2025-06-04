import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

DSM5_ASD_DATA = {
    
    "diagnostic_code": "299.00",
    "diagnosis_name": "Autism Spectrum Disorder",
    "criteria": {
        
        "A": {
            
            "description": """Persistent deficits in social communication and social interaction across multiple contexts, 
            as manifested by the following, currently or by history (examples are illustrative,
            not exhaustive; see text):""",
            "requirements": "All 3 of the following",
            "subcriteria": {
                
                "1.": {
                    
                    "description": "Deficits in social-emotional reciprocity",
                    "examples": [
                        
                        "Abnormal social approach",
                        "Failure of normal back-and-forth conversation",
                        "Reduced sharing of interests, emotions, or affect",
                        "Failure to initiate or respond to social interactions"
                    ]
                },
                "2.": {
                    
                    "description": "Deficits in nonverbal communicative behaviors for social interaction",
                    "examples": [
                        
                        "Poorly integrated verbal and nonverbal communication",
                        "Abnormalities in eye contact and body language",
                        "Deficits in understanding and use of gestures",
                        "Total lack of facial expressions and nonverbal communication"
                    ]
                },
                "3.": {
                    "description": "Deficits in developing, maintaining, and understanding relationships",
                    "examples": [
                        
                        "Difficulties adjusting behavior to suit various social contexts",
                        "Difficulties in sharing imaginative play or making friends",
                        "Absence of interest in peers"
                    ]
                }
            }
        },
        "B": {
            
            "description": """Restricted, repetitive patterns of behavior, interests, or activities, as manifested by at
            least two of the following, currently or by history (examples are illustrative, not exhaus-
            tive; see text):""",
            "requirements": "At least 2 of the following",
            "subcriteria": {
                "1.": {
                    
                    "description": "Stereotyped or repetitive motor movements, use of objects, or speech",
                    "examples": [
                        
                        "Simple motor stereotypies",
                        "Lining up toys or flipping objects",
                        "Echolalia",
                        "Idiosyncratic phrases"
                    ]
                },
                "2.": {
                    "description": "Insistence on sameness, inflexible adherence to routines, or ritualized patterns in behavior",
                    "examples": [
                        
                        "Extreme distress at small changes",
                        "Difficulties with transitions",
                        "Rigid thinking patterns",
                        "Greeting rituals",
                        "Need to take same route or eat same food every day"
                    ]
                },
                "3.": {
                    "description": "Highly restricted, fixated interests that are abnormal in intensity or focus",
                    "examples": [
                        
                        "Strong attachment to or preoccupation with unusual objects",
                        "Excessively circumscribed or perseverative interests"
                    ]
                },
                "4.": {
                    "description": "Hyper- or hyporeactivity to sensory input or unusual interest in sensory aspects of the environment",
                    "examples": [
                        
                        "Apparent indifference to pain/temperature",
                        "Adverse response to specific sounds or textures",
                        "Excessive smelling or touching of objects",
                        "Visual fascination with lights or movement"
                    ]
                }
            }
        },
        "C": {
            
            "description": """Symptoms must be present in the early developmental period (but may not become
                fully manifest until social demands exceed limited capacities, or may be masked by
                learned strategies in later life)."""
        },
        "D": {
            
            "description": """Symptoms cause clinically significant impairment in social, occupational, 
                or other important areas of current functioning."""
        },
        "E": {
            
            "description": """These disturbances are not better explained by intellectual disability 
                (intellectual developmental disorder) or global developmental delay. Intellectual disability and autism
                spectrum disorder frequently co-occur; to make comorbid diagnoses of autism spectrum
                disorder and intellectual disability, social communication should be below that 
                expected for general developmental level."""
        },
        "linked_diagnosis": """Individuals with a well-established DSM-IV diagnosis of autistic disorder, Asperger’s
            disorder, or pervasive developmental disorder not otherwise specified should be given the
            diagnosis of autism spectrum disorder. Individuals who have marked deficits in social
            communication, but whose symptoms do not otherwise meet criteria for autism spectrum
            disorder, should be evaluated for social (pragmatic) communication disorder.""",
        "important_features":[

            "With or without accompanying intellectual impairment",
            "With or without accompanying language impairment",
            "Associated with a known medical or genetic condition or environmental factor",
            "Associated with another neurodevelopmental, mental, or behavioral disorder",
            "With catatonia"
        ],
    },
    "recording_procedures": {

        "description": """For autism spectrum disorder that is associated with a known medical or genetic condition
            or environmental factor, or with another neurodevelopmental, mental, or behavioral disorder, 
            record autism spectrum disorder associated with (name of condition, disorder, or
            factor) (e.g., autism spectrum disorder associated with Rett syndrome). Severity should be
            recorded as level of support needed for each of the two psychopathological domains in
            Severity Table (e.g., “requiring very substantial support for deficits in social communication and
            requiring substantial support for restricted, repetitive behaviors”). Specification of “with
            accompanying intellectual impairment” or “without accompanying intellectual impairment” 
            should be recorded next. Language impairment specification should be recorded
            thereafter. If there is accompanying language impairment, the current level of verbal functioning 
            should be recorded (e.g., “with accompanying language impairment—no intelligible 
            speech” or “with accompanying language impairment—phrase speech”). If catatonia is
            present, record separately “catatonia associated with autism spectrum disorder.”"""
    },
    "specifiers": {
        
        "table_context": """The severity specifiers (see Table 2) may be used to describe succinctly the current symptomatology (which might fall below level 1), with the recognition that severity may vary by
            context and fluctuate over time. Severity of social communication difficulties and restricted, repetitive behaviors should be separately rated. The descriptive severity categories
            should not be used to determine eligibility for and provision of services; these can only bedeveloped at an individual level and through discussion of personal priorities and targets.""",
        "criteria_intellectual_impairment": """Regarding the specifier “with or without accompanying intellectual impairment,” understanding the (often uneven) intellectual profile of a child or adult with autism spectrum
            disorder is necessary for interpreting diagnostic features. Separate estimates of verbal and nonverbal skill are necessary (e.g., using untimed nonverbal tests to assess potential
            strengths in individuals with limited language).""",
        "criteria_language_impairement": """To use the specifier “with or without accompanying language impairment,” the current level of verbal functioning should be assessed and described. Examples of the specific
            descriptions for “with accompanying language impairment” might include no intelligible speech (nonverbal), single words only, or phrase speech. Language level in individuals
            “without accompanying language impairment” might be further described by speaks in full sentences or has fluent speech. Since receptive language may lag behind expressive
            language development in autism spectrum disorder, receptive and expressive language skills should be considered separately.""",
        "condition_association": """The specifier “associated with a known medical or genetic condition or environmental factor” should be used when the individual has a known genetic disorder (e.g., Rett syndrome,
            Fragile X syndrome, Down syndrome), a medical disorder (e.g. epilepsy), or a history of environmental exposure (e.g., valproate, fetal alcohol syndrome, very low birth weight).""",
        "additional_conditions": """Additional neurodevelopmental, mental or behavioral conditions should also be noted (e.g., attention-deficit/hyperactivity disorder; developmental coordination disorder; 
            disruptive behavior, impulse-control, or conduct disorders; anxiety, depressive, or bipolar disorders; tics or Tourette’s disorder; self-injury; feeding, elimination, or sleep disorders)."""
    },
    "severity_table": {
        
        "title": "Severity levels for autism spectrum disorder",
        "severity_level_1": {
            
            "title": "Requiring support",
            "social_communication": """Without supports in place, deficits in social communication cause noticeable impairments.
                Difficulty initiating social interactions, and clear examples of atypical or unsuccessful responses to
                social overtures of others. May appear to have decreased interest in social interactions. For example,
                a person who is able to speak in full sentences and engages in communication but whose to-and-from conversation 
                with others fails, and whose attempts to make friends are odd and typically unsuccessful""",
            "restricted_repetitive_behaviors": """Inflexibility of behavior causes significant interference with functioning in 
                one or more contexts. Difficulty switching between activities. Problems of organization and planning hamper independence."""
        },
        "severity_level_2": {
            
            "title": "Requiring substantial support",
            "social_communication": """Marked deficits in verbal and nonverbal social communication skills; social impairments apparent
                even with supports in place; limited initiation of social interactions; and reduced or abnormal responses to social overtures from others. 
                For example, a person who speaks simple sentences,
                whose interaction is limited to narrow special interests, and who has markedly odd nonverbal communication.""",
            "restricted_repetitive_behaviors": """Inflexibility of behavior, difficulty coping with change, or other restricted/repetitive behaviors
                appear frequently enough to be obvious to the casual observer and interfere with functioning 
                in a variety of contexts. Distress and/or difficulty changing focus or action."""
        },
        "severity_level_3": {
            
            "title": "Requiring very substantial support",
            "social_communication": """Severe deficits in verbal and nonverbal social communication skills cause severe impairments in functioning, 
                very limited initiation of social interactions, and minimal response to social overtures from others. For example, a person with few 
                words of intelligible speech who rarely initiates interaction and, when he or she does, makes unusual approaches to meet needs only and
                responds to only very direct social approaches.""",
            "restricted_repetitive_behaviors": """Inflexibility of behavior, extreme difficulty coping with change, or other restricted/repetitive behaviors 
                markedly interfere with functioning in all spheres. Great distress/difficulty changing focus or action."""
        }
    },
    "diagnostic_features":{

        "essential_features": """The essential features of autism spectrum disorder are persistent impairment in reciprocal
            social communication and social interaction (Criterion A), and restricted, repetitive patterns of behavior, interests, or activities (Criterion B). These symptoms are present from
            early childhood and limit or impair everyday functioning (Criteria C and D). The stage at which functional impairment becomes obvious will vary according to characteristics of
            the individual and his or her environment. Core diagnostic features are evident in the developmental period, but intervention, compensation, and current supports may mask
            difficulties in at least some contexts. Manifestations of the disorder also vary greatly depending on the severity of the autistic condition, developmental level, and chronological age;
            hence, the term spectrum. Autism spectrum disorder encompasses disorders previously referred to as early infantile autism, childhood autism, Kanner’s autism, high-functioning
            autism, atypical autism, pervasive developmental disorder not otherwise specified, childhood disintegrative disorder, and Asperger’s disorder.""",
        "social_impairments": """The impairments in communication and social interaction specified in Criterion A are pervasive and sustained. Diagnoses are most valid and reliable when based on multiple
            sources of information, including clinician’s observations, caregiver history, and, when possible, self-report. Verbal and nonverbal deficits in social communication have varying
            manifestations, depending on the individual’s age, intellectual level, and language ability, as well as other factors such as treatment history and current support. Many individuals
            have language deficits, ranging from complete lack of speech through language delays, poor comprehension of speech, echoed speech, or stilted and overly literal language. Even
            when formal language skills (e.g., vocabulary, grammar) are intact, the use of language for reciprocal social communication is impaired in autism spectrum disorder.""",
        "emotional_engagement_deficit": """Deficits in social-emotional reciprocity (i.e., the ability to engage with others and share thoughts and feelings) are clearly evident in young children with the disorder, who may
            show little or no initiation of social interaction and no sharing of emotions, along with reduced or absent imitation of others’ behavior. What language exists is often one-sided,
            lacking in social reciprocity, and used to request or label rather than to comment, share
            feelings, or converse. In adults without intellectual disabilities or language delays, deficits in social-emotional reciprocity may be most apparent in difficulties processing and 
            responding to complex social cues (e.g., when and how to join a conversation, what not to say). Adults who have developed compensation strategies for some social challenges still
            struggle in novel or unsupported situations and suffer from the effort and anxiety of consciously calculating what is socially intuitive for most individuals.""",
        "nonverbal_communication_deficit": """Deficits in nonverbal communicative behaviors used for social interaction are manifested by absent, reduced, or atypical use of eye contact (relative to cultural norms), 
            gestures, facial expressions, body orientation, or speech intonation. An early feature of autism spectrum disorder is impaired joint attention as manifested by a lack of pointing, showing,
            or bringing objects to share interest with others, or failure to follow someone’s pointing or eye gaze. Individuals may learn a few functional gestures, but their repertoire is smaller
            than that of others, and they often fail to use expressive gestures spontaneously in communication. Among adults with fluent language, the difficulty in coordinating nonverbal
            communication with speech may give the impression of odd, wooden, or exaggerated “body language” during interactions. Impairment may be relatively subtle within 
            individual modes (e.g., someone may have relatively good eye contact when speaking) but noticeable in poor integration of eye contact, gesture, body posture, prosody, and facial expression for social communication.""",
        "relationship_quality_deficit": """Deficits in developing, maintaining, and understanding relationships should be judged against norms for age, gender, and culture. There may be absent, reduced, or 
            atypical social interest, manifested by rejection of others, passivity, or inappropriate approaches that seem aggressive or disruptive. These difficulties are particularly evident in
            young children, in whom there is often a lack of shared social play and imagination (e.g., age-appropriate flexible pretend play) and, later, insistence on playing by very fixed rules.
            Older individuals may struggle to understand what behavior is considered appropriate in one situation but not another (e.g., casual behavior during a job interview), or the different
            ways that language may be used to communicate (e.g., irony, white lies). There may be an apparent preference for solitary activities or for interacting with much younger or older
            people. Frequently, there is a desire to establish friendships without a complete or realistic idea of what friendship entails (e.g., one-sided friendships or friendships based solely on
            shared special interests). Relationships with siblings, co-workers, and caregivers are also important to consider (in terms of reciprocity).""",
        "restricted_repetition": """Autism spectrum disorder is also defined by restricted, repetitive patterns of behavior, interests, or activities (as specified in Criterion B), which show a range of manifestations
            according to age and ability, intervention, and current supports. Stereotyped or repetitive behaviors include simple motor stereotypies (e.g., hand flapping, finger flicking), repetitive 
            use of objects (e.g., spinning coins, lining up toys), and repetitive speech (e.g., echolalia, the delayed or immediate parroting of heard words; use of “you” when referring to
            self; stereotyped use of words, phrases, or prosodic patterns). Excessive adherence to routines and restricted patterns of behavior may be manifest in resistance to change (e.g., 
            distress at apparently small changes, such as in packaging of a favorite food; insistence on adherence to rules; rigidity of thinking) or ritualized patterns of verbal or nonverbal behavior 
            (e.g., repetitive questioning, pacing a perimeter). Highly restricted, fixated interests in autism spectrum disorder tend to be abnormal in intensity or focus (e.g., a toddler
            strongly attached to a pan; a child preoccupied with vacuum cleaners; an adult spending hours writing out timetables). Some fascinations and routines may relate to apparent hyper- or 
            hyporeactivity to sensory input, manifested through extreme responses to specific sounds or textures, excessive smelling or touching of objects, fascination with lights or
            spinning objects, and sometimes apparent indifference to pain, heat, or cold. Extreme reaction to or rituals involving taste, smell, texture, or appearance of food or excessive food
            restrictions are common and may be a presenting feature of autism spectrum disorder.""",
        "adult_behavior_suppression": """Many adults with autism spectrum disorder without intellectual or language disabilities learn to suppress repetitive behavior in public. Special interests may be a source of
            pleasure and motivation and provide avenues for education and employment later in life. Diagnostic criteria may be met when restricted, repetitive patterns of behavior, interests,
            or activities were clearly present during childhood or at some time in the past, even if symptoms are no longer present.""",
        "clinical_severeness": """Criterion D requires that the features must cause clinically significant impairment in social, occupational, or other important areas of current functioning. Criterion E specifies that
            the social communication deficits, although sometimes accompanied by intellectual disability (intellectual developmental disorder), are not in line with the individual’s developmental
            level; impairments exceed difficulties expected on the basis of developmental level.""",
        "psychometrics": """Standardized behavioral diagnostic instruments with good psychometric properties, including caregiver interviews, questionnaires and clinician observation measures, are
            available and can improve reliability of diagnosis over time and across clinicians."""
    },
    "features_supporting_diagnosis": """Many individuals with autism spectrum disorder also have intellectual impairment and/or language impairment (e.g., slow to talk, language comprehension behind production). Even
        those with average or high intelligence have an uneven profile of abilities. The gap between intellectual and adaptive functional skills is often large. Motor deficits are often present, 
        including odd gait, clumsiness, and other abnormal motor signs (e.g., walking on tiptoes). Selfinjury (e.g., head banging, biting the wrist) may occur, and disruptive/challenging behaviors 
        are more common in children and adolescents with autism spectrum disorder than other disorders, including intellectual disability. Adolescents and adults with autism spectrum 
        disorder are prone to anxiety and depression. Some individuals develop catatonic-like motor behavior (slowing and “freezing” mid-action), but these are typically not of the magnitude 
        of a catatonic episode. However, it is possible for individuals with autism spectrum disorder to experience a marked deterioration in motor symptoms and display a full catatonic episode with 
        symptoms such as mutism, posturing, grimacing and waxy flexibility. The risk period for comorbid catatonia appears to be greatest in the adolescent years.""",
    "prevalence": r"""In recent years, reported frequencies for autism spectrum disorder across U.S. and nonU.S. countries have approached 1% of the population, with similar estimates in child and
        adult samples. It remains unclear whether higher rates reflect an expansion of the diagnostic criteria of DSM-IV to include subthreshold cases, increased awareness, differences
        in study methodology, or a true increase in the frequency of autism spectrum disorder.""",
    "age-symptom_correspondence": {
        
        "ages_during_onset": """The age and pattern of onset also should be noted for autism spectrum disorder. Symptoms are typically recognized during the second year of life (12–24 months of age) but may be seen
            earlier than 12 months if developmental delays are severe, or noted later than 24 months if symptoms are more subtle. The pattern of onset description might include information
            about early developmental delays or any losses of social or language skills. In cases where skills have been lost, parents or caregivers may give a history of a gradual or relatively
            rapid deterioration in social behaviors or language skills. Typically, this would occur between 12 and 24 months of age and is distinguished from the rare instances of developmental 
            regression occurring after at least 2 years of normal development (previously described as childhood disintegrative disorder).""",
        "behavioral_display_ages":"""The behavioral features of autism spectrum disorder first become evident in early childhood, with some cases presenting a lack of interest in social interaction in the first
            year of life. Some children with autism spectrum disorder experience developmental plateaus or regression, with a gradual or relatively rapid deterioration in social behaviors or
            use of language, often during the first 2 years of life. Such losses are rare in other disorders and may be a useful “red flag” for autism spectrum disorder. Much more unusual
            and warranting more extensive medical investigation are losses of skills beyond social communication (e.g., loss of self-care, toileting, motor skills) or those occurring after the
            second birthday (see also Rett syndrome in the section “Differential Diagnosis” for this disorder).""",
        "symptom_display_ages": """First symptoms of autism spectrum disorder frequently involve delayed language development, often accompanied by lack of social interest or unusual social interactions (e.g.,
            pulling individuals by the hand without any attempt to look at them), odd play patterns (e.g., carrying toys around but never playing with them), and unusual communication
            patterns (e.g., knowing the alphabet but not responding to own name). Deafness may be suspected but is typically ruled out. During the second year, odd and repetitive behaviors
            and the absence of typical play become more apparent. Since many typically developing young children have strong preferences and enjoy repetition (e.g., eating the same foods,
            watching the same video multiple times), distinguishing restricted and repetitive behaviors that are diagnostic of autism spectrum disorder can be difficult in preschoolers. The
            clinical distinction is based on the type, frequency, and intensity of the behavior (e.g., a child who daily lines up objects for hours and is very distressed if any item is moved).""",
        "deterioration_ages": """Autism spectrum disorder is not a degenerative disorder, and it is typical for learning and compensation to continue throughout life. Symptoms are often most marked in early
            childhood and early school years, with developmental gains typical in later childhood in at least some areas (e.g., increased interest in social interaction). A small proportion of 
            individuals deteriorate behaviorally during adolescence, whereas most others improve. Only a minority of individuals with autism spectrum disorder live and work independently 
            in adulthood; those who do tend to have superior language and intellectual abilities and are able to find a niche that matches their special interests and skills. In general, individuals 
            with lower levels of impairment may be better able to function independently. However, even these individuals may remain socially naive and vulnerable, have difficulties 
            organizing practical demands without aid, and are prone to anxiety and depression. Many adults report using compensation strategies and coping mechanisms to mask their
            difficulties in public but suffer from the stress and effort of maintaining a socially acceptable facade. Scarcely anything is known about old age in autism spectrum disorder.""",
        "diagnosis_ages": """Some individuals come for first diagnosis in adulthood, perhaps prompted by the diagnosis of autism in a child in the family or a breakdown of relations at work or home. Obtaining 
            detailed developmental history in such cases may be difficult, and it is important to consider selfreported difficulties. Where clinical observation suggests criteria are currently met, autism
            spectrum disorder may be diagnosed, provided there is no evidence of good social and communication skills in childhood. For example, the report (by parents or another relative) that the
            individual had ordinary and sustained reciprocal friendships and good nonverbal communication skills throughout childhood would rule out a diagnosis of autism spectrum disorder;
            however, the absence of developmental information in itself should not do so.""",
        "manifestation_clarity": """Manifestations of the social and communication impairments and restricted/repetitive behaviors that define autism spectrum disorder are clear in the developmental period.
            In later life, intervention or compensation, as well as current supports, may mask these difficulties in at least some contexts. However, symptoms remain sufficient to cause current
            impairment in social, occupational, or other important areas of functioning."""
    },
    "risk_and_prognostics": {

        "fundamentals": """The best established prognostic factors for individual outcome within autism spectrum disorder are presence or absence of associated intellectual disability and language impairment 
            (e.g., functional language by age 5 years is a good prognostic sign) and additional mental health problems. Epilepsy, as a comorbid diagnosis, is associated with greater intellectual disability and lower verbal ability.""",
        "prognostic_factors":{
            
            "environmental": """A variety of nonspecific risk factors, such as advanced parental age, low birth weight, or fetal exposure to valproate, may contribute to risk of autism spectrum disorder.""",
            "genetic_and_physiological": r"""Heritability estimates for autism spectrum disorder have ranged from 37% to higher than 90%, based on twin concordance rates. Currently, as many
                as 15% of cases of autism spectrum disorder appear to be associated with a known genetic mutation, with different de novo copy number variants or de novo mutations in specific
                genes associated with the disorder in different families. However, even when an autism spectrum disorder is associated with a known genetic mutation, it does not appear to be
                fully penetrant. Risk for the remainder of cases appears to be polygenic, with perhaps hundreds of genetic loci making relatively small contributions."""
        }
    },
    "diagnosis_issues": {
        
        "culture-related": """Cultural differences will exist in norms for social interaction, nonverbal communication, and relationships, but individuals with autism spectrum disorder are markedly impaired
            against the norms for their cultural context. Cultural and socioeconomic factors may affect age at recognition or diagnosis; for example, in the United States, late or underdiagnosis of
            autism spectrum disorder among African American children may occur.""",
        "gender-related": """Autism spectrum disorder is diagnosed four times more often in males than in females. In clinic samples, females tend to be more likely to show accompanying intellectual disability, 
            suggesting that girls without accompanying intellectual impairments or language delays may go unrecognized, perhaps because of subtler manifestation of social and communication difficulties."""
    },
    "functional_consequences": {
        
        "infant_dysfunctionality": """In young children with autism spectrum disorder, lack of social and communication abilities may hamper learning, especially learning through social interaction or in settings
            with peers. In the home, insistence on routines and aversion to change, as well as sensory sensitivities, may interfere with eating and sleeping and make routine care (e.g., haircuts,
            dental work) extremely difficult. Adaptive skills are typically below measured IQ. Extreme 
            difficulties in planning, organization, and coping with change negatively impact academic achievement, even for students with above-average intelligence. During adulthood, 
            these individuals may have difficulties establishing independence because of continued rigidity and difficulty with novelty.""",
        "adult_dysfunctionality": """Many individuals with autism spectrum disorder, even without intellectual disability, have poor adult psychosocial functioning as indexed by measures such as independent
            living and gainful employment. Functional consequences in old age are unknown, but social isolation and communication problems (e.g., reduced help-seeking) are likely to have consequences for health in older adulthood."""
    },
    "differential_diagnosis": {

        "rett_syndrome": """Disruption of social interaction may be observed during the regressive phase of Rett syndrome (typically between 1–4 years of age); thus, a substantial proportion
            of affected young girls may have a presentation that meets diagnostic criteria for autism spectrum disorder. However, after this period, most individuals with Rett syndrome improve 
            their social communication skills, and autistic features are no longer a major area of concern. Consequently, autism spectrum disorder should be considered only when all diagnostic criteria are met.""",
        "selective_mutism": """In selective mutism, early development is not typically disturbed. The affected child usually exhibits appropriate communication skills in certain contexts
            and settings. Even in settings where the child is mute, social reciprocity is not impaired, nor are restricted or repetitive patterns of behavior present.""", 
        "language_disorders": """In some forms of language disorder, there may be problems of communication and some secondary social difficulties. However, specific language disorder is not usually associated with 
            abnormal nonverbal communication, nor with the presence of restricted, repetitive patterns of behavior, interests, or activities.""",
        "social_communication_disorder": """When an individual shows impairment in social communication and social interactions but does not show restricted and repetitive behavior or interests, criteria for social 
            (pragmatic) communication disorder, instead of autism spectrum disorder, may be met. The diagnosis of autism spectrum disorder supersedes that of social (pragmatic) communication
            disorder whenever the criteria for autism spectrum disorder are met, and care should be taken to enquire carefully regarding past or current restricted/repetitive behavior.""",
        "intellectual_disability_without_autism": """Intellectual disability without autism spectrum disorder may be difficult to differentiate from autism spectrum disorder in very young children. Individuals with in-
            tellectual disability who have not developed language or symbolic skills also present a challenge for differential diagnosis, since repetitive behavior often occurs in such individuals 
            as well. A diagnosis of autism spectrum disorder in an individual with intellectual disability is appropriate when social communication and interaction are significantly im-
            paired relative to the developmental level of the individual’s nonverbal skills (e.g., fine motor skills, nonverbal problem solving). In contrast, intellectual disability is the appropri-
            ate diagnosis when there is no apparent discrepancy between the level of social-communicative skills and other intellectual skills.""",
        "stereotypic_movement_disorder": """Motor stereotypies are among the diagnostic characteristics of autism spectrum disorder, so an additional diagnosis of stereotypic movement
            disorder is not given when such repetitive behaviors are better explained by the presence of autism spectrum disorder. However, when stereotypies cause self-injury and become a
            focus of treatment, both diagnoses may be appropriate.""",
        "attention-deficit_hyperactivity_disorder": """Abnormalities of attention (overly focused or easily distracted) are common in individuals with autism spectrum disorder, as is hy-
            peractivity. A diagnosis of attention-deficit/hyperactivity disorder (ADHD) should be considered when attentional difficulties or hyperactivity exceeds that typically seen in in-
            dividuals of comparable mental age.""",
        "schizophrenia": """Schizophrenia with childhood onset usually develops after a period of normal, or near normal, development. A prodromal state has been described in which social 
            impairment and atypical interests and beliefs occur, which could be confused with the social deficits seen in autism spectrum disorder. Hallucinations and delusions, which are
            defining features of schizophrenia, are not features of autism spectrum disorder. However, clinicians must take into account the potential for individuals with autism spectrum
            disorder to be concrete in their interpretation of questions regarding the key features of schizophrenia (e.g., “Do you hear voices when no one is there?” ”Yes [on the radio]”)."""
    },
    "comorbidity": r"""Autism spectrum disorder is frequently associated with intellectual impairment and structural language disorder (i.e., an inability to comprehend and construct sentences with proper
        grammar), which should be noted under the relevant specifiers when applicable. Many individuals with autism spectrum disorder have psychiatric symptoms that do not form part of
        the diagnostic criteria for the disorder (about 70% of individuals with autism spectrum disorder may have one comorbid mental disorder, and 40% may have two or more comorbid
        mental disorders). When criteria for both ADHD and autism spectrum disorder are met, both diagnoses should be given. This same principle applies to concurrent diagnoses of autism
        spectrum disorder and developmental coordination disorder, anxiety disorders, depressive disorders, and other comorbid diagnoses. Among individuals who are nonverbal 
        or have language deficits, observable signs such as changes in sleep or eating and increases in challenging behavior should trigger an evaluation for anxiety or depression. Specific learning 
        difficulties (literacy and numeracy) are common, as is developmental coordination disorder. Medical conditions commonly associated with autism spectrum disorder should be noted under the “associated 
        with a known medical/genetic or environmental/acquired condition” specifier. Such medical conditions include epilepsy, sleep problems, and constipation. Avoidant-restrictive food intake disorder is 
        a fairly frequent presenting feature of autism spectrum disorder, and extreme and narrow food preferences may persist."""
}

class DSM5MCPServer:
    def __init__(self):
        self.server = Server("dsm5-asd-server")
        self.setup_handlers()
    
#Everything below is unused

    def setup_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available DSM-5 resources"""
            return [
                Resource(
                    uri="dsm5://autism-spectrum-disorder/criteria",
                    name="DSM-5 ASD Diagnostic Criteria",
                    description="Complete diagnostic criteria for Autism Spectrum Disorder",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/recording",
                    name="DSM-5 ASD Recording Procedures",
                    description="Procedure for severity measurement",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/specifiers",
                    name="DSM-5 ASD Specification Explanation",
                    description="Explanation on severity specification",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/severity",
                    name="DSM-5 ASD Severity Specifiers", 
                    description="Severity levels and support requirements",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/diagnostic",
                    name="DSM-5 ASD Diagnostic Features", 
                    description="Features to look for in diagnosis",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/features",
                    name="DSM-5 ASD Features Supporting Diagnosis", 
                    description="Associated features supporting diagnosis",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/prevalence",
                    name="DSM-5 ASD Prevalence", 
                    description="Global case data on ASD",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/age",
                    name="DSM-5 ASD Development and Course", 
                    description="Difference in ASD symptoms at certain ages",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/risk",
                    name="DSM-5 ASD Risks and Prognastic Factors", 
                    description="Causes, indications, and risks of ASD",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/diagnosis",
                    name="DSM-5 ASD Diagnostic Issues", 
                    description="Frequency of ASD cases in certain areas",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/functional",
                    name="DSM-5 ASD Functional Consequences", 
                    description="Functional consequences and regression in ASD",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/differential",
                    name="DSM-5 ASD Differential Diagnosis",
                    description="Conditions to consider in differential diagnosis",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dsm5://autism-spectrum-disorder/comorbidity",
                    name="DSM-5 ASD Comorbidity", 
                    description="Explanation of disorders coexisting with ASD",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read specific DSM-5 resource"""
            if uri == "dsm5://autism-spectrum-disorder/criteria":
                return json.dumps(DSM5_ASD_DATA["criteria"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/recording":
                return json.dumps(DSM5_ASD_DATA["recording_procedures"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/specifiers":
                return json.dumps(DSM5_ASD_DATA["specifiers"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/severity":
                return json.dumps(DSM5_ASD_DATA["severity_specifiers"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/diagnostic":
                return json.dumps(DSM5_ASD_DATA["diagnostic_features"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/features":
                return json.dumps(DSM5_ASD_DATA["features_supporting_diagnosis"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/prevalence":
                return json.dumps(DSM5_ASD_DATA["prevalence"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/age":
                return json.dumps(DSM5_ASD_DATA["age-symptom_correspondence"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/risk":
                return json.dumps(DSM5_ASD_DATA["risk_and_prognostics"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/diagnosis":
                return json.dumps(DSM5_ASD_DATA["diagnosis_issues"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/functional":
                return json.dumps(DSM5_ASD_DATA["functional_consequences"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/differential":
                return json.dumps(DSM5_ASD_DATA["differential_diagnosis"], indent=2)
            elif uri == "dsm5://autism-spectrum-disorder/comorbidity":
                return json.dumps(DSM5_ASD_DATA["comorbidity"], indent=2)
            else:
                raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available diagnostic tools"""
            return [
                
                Tool(
                    name="query_diagnostic_criteria",
                    description="Query specific DSM-5 ASD diagnostic criteria",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "criterion": {
                                "type": "string",
                                "description": "Criterion to query (A, B, C, D, E, or specific subcriteria)"
                            }
                        },
                    "required": ["criterion"]
                }
                ),
                Tool(
                    name="access_recording_procedures",
                    description="Get DSM-5 ASD severity measurement procedures",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "procedure_type": {
                                "type": "string",
                                "description": "Type of recording procedure to access"
                            }
                        },
                        "required": ["procedure_type"]
                    }
                ),
                Tool(
                    name="query_dsm5_specifiers",
                    description="Query DSM-5 Autism Spectrum Disorder specifiers and severity levels",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "specifier_type": {
                                "type": "string",
                                "description": "Type of specifier to query (e.g., 'severity_levels', 'associated_features', 'course_modifiers')",
                                "enum": ["severity_levels", "associated_features", "course_modifiers", "all"]
                            }
                        },
                        "required": ["specifier_type"]
                    }
                ),
                Tool(
                    name="get_severity_specifiers",
                    description="Retrieve DSM-5 ASD severity levels and support requirements",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "enum": ["social_communication", "restricted_repetitive_behaviors", "overall"],
                                "description": "Domain for severity assessment"
                            }
                        },
                        "required": ["domain"]
                    }
                ),
                Tool(
                    name="analyze_diagnostic_features",
                    description="Analyze specific diagnostic features for ASD identification",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature_category": {
                                "type": "string",
                                "description": "Category of diagnostic features to analyze"
                            },
                            "patient_data": {
                                "type": "object",
                                "description": "Patient observation data from multi-modal analysis"
                            }
                        },
                        "required": ["feature_category", "patient_data"]
                    }
                ),
                Tool(
                    name="assess_supporting_features",
                    description="Assess associated features that support ASD diagnosis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "observations": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Observed behaviors and characteristics"
                            }
                        },
                        "required": ["observations"]
                    }
                ),
                Tool(
                    name="check_prevalence_data",
                    description="Access global prevalence data for ASD",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "demographic": {
                                "type": "string",
                                "description": "Specific demographic to query (age, gender, geographic)"
                            }
                        },
                        "required": ["demographic"]
                    }
                ),
                Tool(
                    name="analyze_age_symptoms",
                    description="Analyze ASD symptom presentation at different ages",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "patient_age": {
                                "type": "number",
                                "description": "Patient's current age"
                            },
                            "developmental_stage": {
                                "type": "string",
                                "enum": ["early_childhood", "school_age", "adolescence", "adulthood"],
                                "description": "Developmental stage for symptom analysis"
                            }
                        },
                        "required": ["patient_age", "developmental_stage"]
                    }
                ),
                Tool(
                    name="evaluate_risk_factors",
                    description="Evaluate risk and prognostic factors for ASD",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "factor_type": {
                                "type": "string",
                                "enum": ["genetic", "environmental", "temperamental", "course_modifiers"],
                                "description": "Type of risk factor to evaluate"
                            },
                            "patient_history": {
                                "type": "object",
                                "description": "Patient's medical and family history"
                            }
                        },
                        "required": ["factor_type", "patient_history"]
                    }
                ),
                Tool(
                    name="address_diagnostic_issues",
                    description="Address culture-related and gender-related diagnostic issues",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "issue_type": {
                                "type": "string",
                                "enum": ["culture_related", "gender_related", "diagnostic_markers"],
                                "description": "Type of diagnostic issue to address"
                            },
                            "patient_demographics": {
                                "type": "object",
                                "description": "Patient demographic information"
                            }
                        },
                        "required": ["issue_type", "patient_demographics"]
                    }
                ),
                Tool(
                    name="assess_functional_consequences",
                    description="Assess functional consequences and regression patterns in ASD",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "functional_domain": {
                                "type": "string",
                                "enum": ["social", "academic", "occupational", "adaptive"],
                                "description": "Functional domain to assess"
                            },
                            "current_functioning": {
                                "type": "object",
                                "description": "Current level of functioning data"
                            }
                        },
                        "required": ["functional_domain", "current_functioning"]
                    }
                ),
                Tool(
                    name="perform_differential_diagnosis",
                    description="Perform differential diagnosis to rule out other conditions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "presenting_symptoms": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Primary symptoms to differentiate"
                            },
                            "differential_conditions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Conditions to consider in differential"
                            }
                        },
                        "required": ["presenting_symptoms"]
                    }
                ),
                Tool(
                    name="evaluate_comorbidity",
                    description="Evaluate potential comorbid conditions with ASD",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symptom_profile": {
                                "type": "object",
                                "description": "Complete symptom profile from multi-modal analysis"
                            },
                            "comorbid_indicators": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Indicators suggesting potential comorbid conditions"
                            }
                        },
                        "required": ["symptom_profile"]
                    }
                ),
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Handle tool calls for DSM-5 analysis"""
            
            if name == "query_diagnostic_criteria":
                criterion = arguments.get("criterion", "").upper()
                
                if criterion in DSM5_ASD_DATA["criteria"]:
                    result = DSM5_ASD_DATA["criteria"][criterion]
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                for main_criterion, details in DSM5_ASD_DATA["criteria"].items():
                    if "subcriteria" in details and criterion in details["subcriteria"]:
                        result = details["subcriteria"][criterion]
                        return [types.TextContent(
                            type="text", 
                            text=json.dumps(result, indent=2)
                        )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Criterion {criterion} not found"
                )]
            
            elif name == "access_recording_procedures":
                procedure_type = arguments.get("procedure_type", "")
                
                if procedure_type in DSM5_ASD_DATA["recording_procedures"]:
                    result = DSM5_ASD_DATA["recording_procedures"][procedure_type]
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Recording procedure type '{procedure_type}' not found"
                )]
            
            elif name == "query_dsm5_specifiers":
                specifier_type = arguments.get("specifier_type", "")
            
                if specifier_type == "all":
                    result = DSM5_ASD_DATA["specifiers"]
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif specifier_type in DSM5_ASD_DATA["specifiers"]:
                    result = DSM5_ASD_DATA["specifiers"][specifier_type]
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
            
                return [types.TextContent(
                    type="text",
                    text=f"Specifier type '{specifier_type}' not found"
                )]
            
            elif name == "get_severity_specifiers":
                domain = arguments.get("domain", "")
                
                if domain in DSM5_ASD_DATA["severity_specifiers"]:
                    result = DSM5_ASD_DATA["severity_specifiers"][domain]
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Severity domain '{domain}' not found"
                )]

            elif name == "analyze_diagnostic_features":
                feature_category = arguments.get("feature_category", "")
                patient_data = arguments.get("patient_data", {})
                
                if feature_category in DSM5_ASD_DATA["diagnostic_features"]:
                    features = DSM5_ASD_DATA["diagnostic_features"][feature_category]
                    analysis_result = {
                        "feature_category": feature_category,
                        "diagnostic_features": features,
                        "patient_data_analysis": patient_data,
                        "matches": []
                    }
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(analysis_result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Diagnostic feature category '{feature_category}' not found"
                )]

            elif name == "assess_supporting_features":
                observations = arguments.get("observations", [])
                
                supporting_features = DSM5_ASD_DATA["features_supporting_diagnosis"]
                assessment_result = {
                    "observations": observations,
                    "supporting_features": supporting_features,
                    "matches": [],
                    "confidence_score": 0.0
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(assessment_result, indent=2)
                )]

            elif name == "check_prevalence_data":
                demographic = arguments.get("demographic", "")
                
                prevalence_data = DSM5_ASD_DATA["prevalence"]
                if demographic in prevalence_data:
                    result = prevalence_data[demographic]
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(prevalence_data, indent=2)
                )]

            elif name == "analyze_age_symptoms":
                patient_age = arguments.get("patient_age", 0)
                developmental_stage = arguments.get("developmental_stage", "")
                
                age_symptom_data = DSM5_ASD_DATA["age-symptom_correspondence"]
                
                if developmental_stage in age_symptom_data:
                    stage_data = age_symptom_data[developmental_stage]
                    analysis_result = {
                        "patient_age": patient_age,
                        "developmental_stage": developmental_stage,
                        "expected_symptoms": stage_data,
                        "age_appropriate_considerations": []
                    }
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(analysis_result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Developmental stage '{developmental_stage}' not found"
                )]

            elif name == "evaluate_risk_factors":
                factor_type = arguments.get("factor_type", "")
                patient_history = arguments.get("patient_history", {})
                
                risk_data = DSM5_ASD_DATA["risk_and_prognostics"]
                
                if factor_type in risk_data:
                    risk_factors = risk_data[factor_type]
                    evaluation_result = {
                        "factor_type": factor_type,
                        "risk_factors": risk_factors,
                        "patient_history": patient_history,
                        "identified_risks": [],
                        "prognostic_indicators": []
                    }
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(evaluation_result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Risk factor type '{factor_type}' not found"
                )]

            elif name == "address_diagnostic_issues":
                issue_type = arguments.get("issue_type", "")
                patient_demographics = arguments.get("patient_demographics", {})
                
                diagnostic_issues = DSM5_ASD_DATA["diagnosis_issues"]
                
                if issue_type in diagnostic_issues:
                    issue_data = diagnostic_issues[issue_type]
                    result = {
                        "issue_type": issue_type,
                        "diagnostic_considerations": issue_data,
                        "patient_demographics": patient_demographics,
                        "specific_recommendations": []
                    }
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Diagnostic issue type '{issue_type}' not found"
                )]

            elif name == "assess_functional_consequences":
                functional_domain = arguments.get("functional_domain", "")
                current_functioning = arguments.get("current_functioning", {})
                
                functional_data = DSM5_ASD_DATA["functional_consequences"]
                
                if functional_domain in functional_data:
                    domain_data = functional_data[functional_domain]
                    assessment_result = {
                        "functional_domain": functional_domain,
                        "expected_consequences": domain_data,
                        "current_functioning": current_functioning,
                        "impairment_level": "",
                        "support_needs": []
                    }
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(assessment_result, indent=2)
                    )]
                
                return [types.TextContent(
                    type="text",
                    text=f"Functional domain '{functional_domain}' not found"
                )]

            elif name == "perform_differential_diagnosis":
                presenting_symptoms = arguments.get("presenting_symptoms", [])
                differential_conditions = arguments.get("differential_conditions", [])
                
                differential_data = DSM5_ASD_DATA["differential_diagnosis"]
                
                differential_result = {
                    "presenting_symptoms": presenting_symptoms,
                    "differential_conditions": differential_conditions,
                    "dsm5_differential_criteria": differential_data,
                    "ruled_out_conditions": [],
                    "requires_further_assessment": [],
                    "diagnostic_confidence": {}
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(differential_result, indent=2)
                )]

            elif name == "evaluate_comorbidity":
                symptom_profile = arguments.get("symptom_profile", {})
                comorbid_indicators = arguments.get("comorbid_indicators", [])
                
                comorbidity_data = DSM5_ASD_DATA["comorbidity"]
                
                comorbidity_result = {
                    "symptom_profile": symptom_profile,
                    "comorbid_indicators": comorbid_indicators,
                    "potential_comorbidities": comorbidity_data,
                    "identified_comorbidities": [],
                    "severity_interactions": {},
                    "treatment_implications": []
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(comorbidity_result, indent=2)
                )]

            elif name == "generate_comprehensive_assessment":
                video_analysis = arguments.get("video_analysis", {})
                audio_analysis = arguments.get("audio_analysis", {})
                history_analysis = arguments.get("history_analysis", {})
                
                comprehensive_result = {
                    "multi_modal_analysis": {
                        "video_analysis": video_analysis,
                        "audio_analysis": audio_analysis,
                        "history_analysis": history_analysis
                    },
                    "diagnostic_criteria_assessment": {},
                    "severity_determination": {},
                    "differential_diagnosis": {},
                    "comorbidity_assessment": {},
                    "functional_impact": {},
                    "diagnostic_conclusion": {
                        "primary_diagnosis": "",
                        "specifiers": [],
                        "severity_level": "",
                        "confidence_score": 0.0,
                        "supporting_evidence": [],
                        "recommendations": []
                    }
                }
                        
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    def generate_dsm5_context(self, patient_data: dict, demographics: dict = {}, comorbid_hints: list = []):
        async def gather():
            results = []

            diagnostic = await self.server.server.call_tool(
                name="analyze_diagnostic_features",
                arguments={"feature_category": "essential_features", "patient_data": patient_data}
            )
            results.append(("Feature Matches", diagnostic[0].text))

            supporting = await self.server.server.call_tool(
                name="assess_supporting_features",
                arguments={"observations": list(patient_data.values())}
            )
            results.append(("Supporting Features", supporting[0].text))

            if comorbid_hints:
                comorbidity = await self.server.server.call_tool(
                    name="evaluate_comorbidity",
                    arguments={
                        "symptom_profile": patient_data,
                        "comorbid_indicators": comorbid_hints
                    }
                )
                results.append(("Comorbidity Assessment", comorbidity[0].text))

            if demographics:
                diagnostic_issues = await self.server.server.call_tool(
                    name="address_diagnostic_issues",
                    arguments={
                        "issue_type": "gender_related",
                        "patient_demographics": demographics
                    }
                )
                results.append(("Gender-Based Diagnostic Considerations", diagnostic_issues[0].text))

            return results

        raw_results = asyncio.run(gather())

        formatted = "\n\n".join(f"### {title} ###\n{section}" for title, section in raw_results)
        return formatted
