# Synthetic platform data

Every CSV in this folder is fabricated for teaching and software testing. It is
not evidence from a BeagleBone, sensor, lamp, relay, or horn. The
`data_origin` column is therefore `synthetic-example` in every row.

The files share the schema written by `tej_platform.event_log.EventLogger`:

- UTC timestamp and elapsed seconds;
- controller system, state, and transition event;
- logical inputs and outputs stored as 0 or 1;
- optional ambient value and unit;
- explicit data origin.

Students preserve their raw log, use a new filename for cleaned data, and never
change `data_origin` to `physical-gpio` unless the values actually came from an
approved physical run.
