# GP Patient Survey 2025 — full questionnaire

Transcribed from the official GPPS 2025 questionnaire (gp-patient.co.uk). Where the question
feeds the practice-level public data file, the variable stem is given in brackets — append
`_N.pct` for category shares or `.pcteval` for the headline positive score.

## Your GP practice services

**Q1** Generally, how easy or difficult is it to contact your GP practice on the phone? `[localgpservicesphone]`
I haven't tried / Very easy / Fairly easy / Neither / Fairly difficult / Very difficult

**Q2** Generally, how easy or difficult is it to contact your GP practice using their website? `[localgpserviceswebsite]`
(same options)

**Q3** Generally, how easy or difficult is it to contact your GP practice using the NHS App? `[localgpservicesapp]`
(same options)

**Q4** Overall, how helpful do you find the reception and administrative team at your GP practice? `[localgpservicesreception]`
Very helpful / Fairly helpful / Not very helpful / Not at all helpful / I don't know

**Q5** Which of the following online GP services have you used in the last 12 months? (multi) `[localgpservicesused]`
Booking appointments / Filling in an online form about a health issue / Ordering repeat
prescriptions / Accessing medical records / Registering with a practice / Finding out test
results / Making an administrative request / None of these

**Q6** Is there a particular healthcare professional at your GP practice you usually prefer to see or speak to? `[localgpservicesprefhp]`
Yes / No (→Q8)

**Q7** How often do you get to see or speak to your preferred healthcare professional when you ask to? `[localgpservicesprefhpsee]` ← *continuity measure used in our models*
Always or almost always / A lot of the time / Sometimes / Never or almost never / I haven't tried

## Your last contact

**Q8** When did you last try to contact your GP practice for yourself or someone else? `[gpcontactwhen]`
In the last 3 months / 3–6 months ago / 6–12 months ago / More than 12 months ago / Haven't contacted since registered (→Q17)

**Q9** On that occasion, what was your main reason for trying to contact your GP practice? `[gpcontactmainreason]`
New health issue / Existing health issue / Prescription / Test results / Administrative request /
Fit note or medical evidence / Discuss specialist referral / Register as new patient / Something else

**Q10** How did you try to contact them? `[gpcontacthow]`
Phoned (→Q11) / Visited in person / Online via practice website / Online via NHS App / Online via other website or app (→Q12) / Another way

**Q11** What happened when you phoned your GP practice on that occasion? `[gpcontactoutcome]`
Answered straight away / Held in queue and waited / Held in queue, asked for automated call-back /
Held in queue but didn't wait (→Q15) / Call wasn't answered at all (→Q15)

**Q12** Once you had contacted your GP practice, did you know what the next step in dealing with your request would be? `[gpcontactnextstep]`
Yes / No / Told to contact practice again another day, they couldn't help that day (→Q15) / Couldn't contact my practice (→Q15)

**Q13** How soon after you contacted your GP practice did you know what the next step would be? `[gpcontactnextsteptiming]`
There and then / Later on the same day / The next day / After two or more days / Can't remember

**Q14** How did your GP practice deal with your request? (multi) `[gpcontacthandlerequest]`
Booked in for an appointment / Given information on managing the issue / Prescribed medication /
Told to go to a pharmacy / Told to contact NHS 111 or different NHS service / Told to get urgent
care / Given help another way / Don't know or can't remember

**Q15** What did you do when you couldn't contact your GP practice or didn't know what the next step would be? (multi) `[gpcontactunsuccessful]`
Tried again / Self-treated / Asked friend or family / Pharmacy / Phoned NHS 111 / NHS 111 online /
Looked online / A&E / Urgent treatment centre / Different NHS service / Advice elsewhere / Nothing

**Q16** Overall, how would you describe your experience of contacting your GP practice on this occasion? `[gpcontactoverall]`
Very good / Fairly good / Neither / Fairly poor / Very poor

## Your last appointment

**Q17** When was your last GP practice appointment? `[lastgpapptlengthgap]`
In the last 3 months / 3–6 months / 6–12 months / More than 12 months / Never since registering (→Q32)

**Q18** Did you do any of the following before trying to get an appointment? (multi) `[lastgpapptaction]`
Self-treated / Asked friend or family / Pharmacy / NHS 111 phone / NHS 111 online / Looked online /
Different NHS service / Advice elsewhere / Nothing

**Q19** Were you offered the following choices? (multi) `[lastgpapptchoice]`
Choice of time or day / Choice of location / Not offered these choices / Didn't need a choice / Can't remember

**Q20** How long after you first contacted your GP practice did the appointment take place? `[lastgpapptwhen]` ← *patient-experienced same-day measure (_1 = same day)*
On the same day / On the next day / A few days later / Between a week and two weeks later /
More than two weeks later / Can't remember

**Q21** How do you feel about how long you waited for your appointment? `[lastgpapptwait]`
It was about right / It took too long / (don't know)

**Q22** How did the appointment take place? `[lastgpappttype]`
Over the phone / Face-to-face at my GP practice / Face-to-face at a different general practice
location / Face-to-face at my home / Over a video call / By text message / By online message

**Q23** Who did you have the appointment with? `[lastgpapptwho]`
A GP / A nurse / A pharmacist working in my GP practice / A mental health professional /
Another healthcare professional / I don't know

**Q24** How good was the healthcare professional at listening to you? `[lastgpapptlisten]`
Very good / Fairly good / Neither / Fairly poor / Very poor / Don't know or didn't apply

**Q25** How good was the healthcare professional at treating you with care and concern? `[lastgpapptcare]`
(same options)

**Q26** How good was the healthcare professional at considering your mental wellbeing? `[lastgpapptmental]`
(same options)

**Q27** Did you feel the healthcare professional had all the information they needed about you? `[lastgpapptinfo]`
Yes definitely / Yes to some extent / No not at all / Don't know or didn't apply

**Q28** Did you have confidence and trust in the healthcare professional? `[lastgpapptconf]`
(same options)

**Q29** Were you involved as much as you wanted to be in decisions about your care and treatment? `[lastgpapptdecision]`
Yes definitely / Yes to some extent / No not at all / Can't remember or didn't apply

**Q30** What was the outcome of the appointment? (multi) `[lastgpapptoutcome]`
Prescription / Referred for specialist care / Future appointment at practice / Information or
advice for home management / Asked for more information / Advised to re-contact if worse /
Something else / No further action / Can't remember

**Q31** Thinking about the reason for your last appointment, were your needs met? `[lastgpapptneeds]`
Yes definitely / Yes to some extent / No not at all / Don't know

## Overall experience

**Q32** Overall, how would you describe your experience of your GP practice? `[overallexp]` ← *satisfaction measure used in our models*
Very good / Fairly good / Neither / Fairly poor / Very poor

## When your GP practice is closed

**Q33** In the last 12 months, have you contacted or used an NHS service when you wanted care from your GP practice but it was closed? (multi) `[gpcloseduse]`
Yes for myself / Yes for someone else / No (→Q37)

**Q34** Which services did you contact or use on that occasion? (multi) `[gpclosedservices]`
NHS 111 phone / NHS 111 online / Different NHS website / GP practice website / A&E /
Urgent treatment centre / Pharmacy / Different NHS service / Can't remember

**Q35** How do you feel about how long you waited to get care or advice on that occasion? `[gpclosedwait]`
About right / Took too long / Don't know or doesn't apply

**Q36** Overall, how would you describe your experience of NHS services on this occasion? `[gpclosedoverall]`
Very good / Fairly good / Neither / Fairly poor / Very poor

## Your health

**Q37** Have you experienced any of the following in the last 12 months? (multi) `[healthexperienced]`
Problems with physical mobility / Two or more falls needing medical attention / Feeling isolated / None

**Q38** Do you have any physical or mental health conditions lasting or expected to last 12 months or more? `[healthltcondition]`
Yes / No / Don't know / Prefer not to say (→Q40)

**Q39** Which long-term conditions do you have? (multi) `[healthconditionre]`
Arthritis or back/joint problem / Autism spectrum / Blindness or partial sight / Cancer in last
5 years / Deafness or hearing loss / Dementia or Alzheimer's / Diabetes / Heart or cardiovascular /
High blood pressure / Kidney or liver disease / Learning disability / Lung or breathing condition /
Mental health condition / Neurological condition / Stroke or TIA / Another / None

**Q40** Would you describe yourself as having 'long COVID'? `[healthlongcovid]`
Yes / No / Don't know / Prefer not to say

**Q41** Do any of your conditions reduce your ability to carry out day-to-day activities? `[healthimpact]`
Yes a lot / Yes a little / No not at all

**Q42** How confident are you that you can manage issues caused by your conditions? `[healthconfidence]`
Very / Fairly / Not very / Not at all confident / Don't know

**Q43** In the last 12 months, have you had enough support from local services to manage your conditions? `[healthsupport]`
Yes definitely / Yes to some extent / No / Haven't needed support / Don't know

**Q44** Have you had a conversation with a healthcare professional from your GP practice about what is important to you in managing your conditions? `[healthconversation]`
Yes (→Q45) / No / Don't know (→Q47)

**Q45** Have you agreed a plan with a healthcare professional from your GP practice to manage your conditions? `[healthcareplan]`
Yes / No / Don't know (→Q47)

**Q46** How helpful have you found this plan? `[healthcareplanhelpful]`
Very / Fairly / Not very / Not at all helpful / Don't know

## Pharmacy

**Q47** In the last 12 months, which services have you used a pharmacy for? (multi) `[pharmacyused]`
Referred issue from GP/111/A&E / Pick up prescription / Buy medication / Get advice /
Blood pressure check / Vaccine / Contraception without GP prescription / Long-term condition
monitoring or support / None

**Q48** How would you describe your experience of using these pharmacy services? `[pharmacyoverall]`
Very good / Fairly good / Neither / Fairly poor / Very poor

## Dentistry (not in practice-level file)

**Q49** When did you last try to get an NHS dental appointment for yourself?
**Q50** Was it with a dental practice you had been to before for NHS care?
**Q51** Were you able to get an NHS dental appointment? (multi)
**Q52** Overall, how would you describe your experience of NHS dental services?
**Q53** Why haven't you tried to get an NHS dental appointment in the last two years?

## About you (demographics; aboutyou* stems)

**Q54** Age band `[aboutyouagemerged]` — Under 16 … 85 or over
**Q55** Gender `[aboutyougender]` — Female / Male / Non-binary / Self-describe / Prefer not to say
**Q56** Gender identity same as sex registered at birth `[aboutyougenderidentitysex]`
**Q57** Sexual orientation `[aboutyousexualorientation]`
**Q58** Ethnic group `[aboutyouethnicity]` (also `dv_ethnicityband`)
**Q59** Religion `[aboutyoureligion]`
**Q60** Work status (multi) `[aboutyouworkstatus]`
**Q61** Carer responsibilities `[aboutyoucarer]`
**Q62** Parent/guardian of children under 16 `[aboutyouparent]`
**Q63** Smoking habits `[aboutyousmoking]`
**Q64** Vaping habits `[aboutyouvaping]` (in data file; question follows smoking)

---
*Fieldwork: Jan–Mar 2025 (published July 2025). The 2024 survey used the same redesigned
questionnaire; 2023 and earlier used the pre-redesign questionnaire and are not directly
comparable for most items. Practice file also carries `distributed`, `received`, `resprate`,
`popsize` and admin identifiers (`ad_practicecode` etc.).*
