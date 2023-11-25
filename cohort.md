### Features
#### Baseline(9 features)
- age_now, gender, insurance, race, admission_type, first_careunit, weight_kg, height_cm, tobacco

```sql=
WITH baseline AS (
  SELECT 
  c.subject_id,
  c.stay_id,
  a.hadm_id,
  p.gender,
  a.race,
  a.admission_type,
  a.insurance,
  icu.first_careunit,
  EXTRACT(YEAR FROM icu.intime) - p.anchor_year + p.anchor_age AS age_now,
  FROM `physionet-data-399614.2840.cohort` as c
  JOIN `physionet-data.mimiciv_hosp.patients` as p ON p.subject_id = c.subject_id
  JOIN `physionet-data.mimiciv_icu.icustays` as icu ON icu.subject_id = c.subject_id AND icu.stay_id = c.stay_id
  JOIN `physionet-data.mimiciv_hosp.admissions` as a ON a.subject_id = c.subject_id AND a.hadm_id = icu.hadm_id
),
weight_height_tobacco AS (
  WITH all_weight_height_tobacco AS (
    SELECT
    c.stay_id,
    (CASE WHEN c_event.itemid = 226512 THEN c_event.value ELSE NULL END) AS weight_kg,
    (CASE WHEN c_event.itemid = 226730 THEN c_event.value ELSE NULL END) AS height_cm,
    (CASE WHEN c_event.itemid = 227687 THEN 1 ELSE 0 END) AS tobacco
    FROM `physionet-data-399614.2840.cohort` as c
    JOIN `physionet-data.mimiciv_icu.chartevents` AS c_event ON c.stay_id = c_event.stay_id
  )
  SELECT stay_id, MAX(weight_kg) as weight_kg, MAX(height_cm) as height_cm, MAX(tobacco) as tobacco
  FROM all_weight_height_tobacco
  GROUP BY stay_id
)

SELECT
subject_id,
baseline.stay_id,
hadm_id,
age_now,
gender,
insurance,
race,
admission_type,
first_careunit,
weight_kg,
height_cm,
tobacco,
FROM baseline
JOIN weight_height_tobacco ON baseline.stay_id = weight_height_tobacco.stay_id
```
#### Charttime
- ventilator_setting: peep, fio2, tidal_volume_observed, respiratory_rate_set, plateau_pressure
```sql=
WITH ven_setting AS (
  SELECT
  c.stay_id,
  c.subject_id,
  charttime,
  peep,
  fio2,
  tidal_volume_observed,
  respiratory_rate_set,
  plateau_pressure,
  ventilator_type,
  FROM `physionet-data-399614.2840.cohort` as c
  JOIN `physionet-data.mimiciv_derived.ventilator_setting` AS v ON c.stay_id = v.stay_id
)
SELECT * FROM ven_setting
```
- O2_flow
```sql=
WITH O2_flow AS (
  SELECT
  c.stay_id,
  c.subject_id,
  charttime,
  (CASE WHEN l.itemid = 50821 THEN l.value ELSE NULL END) AS O2_flow,
  FROM `physionet-data-399614.2840.cohort` as c
  JOIN `physionet-data.mimiciv_hosp.labevents` as l ON l.subject_id = c.subject_id
)
SELECT * FROM O2_flow
WHERE O2_flow.O2_flow IS NOT NULL
ORDER BY stay_id, charttime

```
- urine_output
```sql=
WITH urine_output AS (
  SELECT
  c.stay_id,
  c.subject_id,
  charttime,
  urineoutput
  FROM `physionet-data-399614.2840.cohort` as c
  JOIN `physionet-data.mimiciv_derived.urine_output` AS u ON c.stay_id = u.stay_id
)
SELECT * FROM urine_output
```

- Anion Gap

```sql=
WITH Anion AS (
  SELECT
  c.stay_id,
  c.subject_id,
  charttime,
  value
  FROM `physionet-data-399614.2840.cohort` as c
  JOIN `physionet-data.mimiciv_icu.icustays` AS u ON c.stay_id = u.stay_id
  JOIN `physionet-data.mimiciv_hosp.labevents` AS l ON u.hadm_id = l.hadm_id
  WHERE itemid = 50868 or itemid = 52500
)
SELECT * FROM Anion
```
- GCS

```sql=
WITH GCS AS (
  SELECT
  c.stay_id,
  c.subject_id,
  charttime,
  u.charttime,
  u.valuenum
  FROM `physionet-data-399614.2840.cohort` as c
  JOIN `physionet-data.mimiciv_icu.chartevents` AS u ON c.stay_id = u.stay_id
  WHERE u.itemid = 220739 or u.itemid = 223900 or u.itemid = 223901
)
SELECT * FROM GCS
```
- CHF

```sql=
WITH CHF AS (
  SELECT
  c.stay_id,
  c.subject_id,
  FROM `physionet-data-399614.2840.cohort` as c
  JOIN `physionet-data.mimiciv_hosp.diagnoses_icd` AS u ON c.subject_id = u.subject_id
  WHERE u.icd_code = '4280'
)
SELECT * FROM CHF
```

- vitalsign: heart_rate, sbp, dbp, mbp, resp_rate, spo2
```sql=
WITH vitalsign AS (
  SELECT 
  c.subject_id,
  c.stay_id,
  vital.charttime,
  vital.heart_rate,
  vital.sbp,
  vital.dbp,
  vital.mbp,
  vital.resp_rate,
  vital.spo2
  FROM `dh-project-00.sepsis_cohort_v1.sepsis_cohort_subject_id_stay_id` as c
  JOIN `physionet-data.mimiciv_derived.vitalsign` as vital ON vital.stay_id = c.stay_id
)
SELECT * FROM vitalsign
```
- RSBI and Minute_ventilation
	- RSBI during SBT vs. during MV
		- RSBI = Tidal volume / respiratory rate
	- Minute ventilation SBT vs. during MV 
		- Minute ventilation = Tidal volume * respiratory rate
	- These two features generate after fix into 24 rows for each patients (already have `tidal_volume_observed` and `resp_rate` from vitalsign)