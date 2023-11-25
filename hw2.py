'''

SELECT base.stay_id, charttime, urineoutput, label FROM `physionet-data-399614.2840.hw2` as base
LEFT JOIN `physionet-data.mimiciv_derived.urine_output` as uo
on base.stay_id = uo.stay_id


SELECT distinct(base.stay_id), label FROM `physionet-data-399614.2840.hw2` as base
INNER JOIN `physionet-data.mimiciv_derived.vasopressin` as va
on base.stay_id = va.stay_id


SELECT base.subject_id, base.stay_id, p.gender, base.label FROM `physionet-data-399614.2840.hw2` as base
LEFT JOIN  `physionet-data.mimiciv_hosp.patients`  as p
on base.subject_id = p.subject_id


SELECT base.subject_id, base.stay_id, value, valuenum, label FROM `physionet-data-399614.2840.hw2` as base
LEFT JOIN  `physionet-data.mimiciv_hosp.labevents`  as lab
on base.subject_id = lab.subject_id
WHERE lab.itemid = 50811


SELECT distinct base.subject_id, base.stay_id,resp_rate,heart_rate, glucose, label FROM `physionet-data-399614.2840.hw2` as base
LEFT JOIN  `physionet-data.mimiciv_derived.vitalsign`  as vit
on base.subject_id = vit.subject_id

'''