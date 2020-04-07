CREATE SCHEMA IF NOT EXISTS face_analysis AUTHORIZATION postgres;
SET SEARCH_PATH TO face_analysis;
CREATE TABLE IF NOT EXISTS face_analysis.results (
	uuid uuid NOT NULL,
	nearest_faces json NOT NULL,
	CONSTRAINT results_pk PRIMARY KEY (uuid)
);
