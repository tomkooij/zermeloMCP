"""Zermelo API endpoint catalogue, generated from https://docs.zportal.nl/docs/ (supported fields and filters only).

Each entry: title, fields (name, title, type, filterable) and extra filters (name, description, type).
"""

from typing import Any, Dict

ENDPOINTS: Dict[str, Dict[str, Any]] = {
    'appointments': {
        "title": 'Afspraakversies',
        "fields": [
            ('appointmentInstance', 'Afspraak ID', 'long', True),
            ('appointmentLastModified', 'Laatst gewijzigd', 'timestamp', False),
            ('branchOfSchool', 'Vestiging', 'long', True),
            ('cancelled', 'Uitval', 'boolean', True),
            ('changeDescription', 'Wijzigingen', 'string', True),
            ('choosableInDepartmentCodes', 'Vak-op-afdeling', 'string[]', False),
            ('content', 'Onderwerp van de afspraak', 'string', False),
            ('created', 'Aangemaakt', 'timestamp', True),
            ('end', 'Eindtijd', 'timestamp', True),
            ('endTimeSlot', 'Laatste lesuur', 'integer', True),
            ('endTimeSlotName', 'Laatste lesuur', 'string', True),
            ('groupChanged', 'Groep gewijzigd', 'boolean', True),
            ('groups', 'Groep', 'string[]', False),
            ('hidden', 'Verwijderd', 'boolean', True),
            ('id', 'ID', 'long', True),
            ('lastModified', 'Laatst gewijzigd', 'timestamp', False),
            ('locationChanged', 'Lokaal gewijzigd', 'boolean', True),
            ('locations', 'Lokalen', 'string[]', False),
            ('optional', 'Keuzeles', 'boolean', True),
            ('schedulerRemark', 'Opmerking van de roostermaker', 'string', True),
            ('start', 'Starttijd', 'timestamp', True),
            ('startTimeSlot', 'Eerste lesuur', 'integer', True),
            ('startTimeSlotName', 'Eerste lesuur', 'string', True),
            ('students', 'Leerlingen', 'string[]', False),
            ('subjects', 'Vak', 'string[]', True),
            ('teacherChanged', 'Docent gewijzigd', 'boolean', True),
            ('teachers', 'Docent', 'string[]', True),
            ('timeChanged', 'Tijd gewijzigd', 'boolean', True),
            ('type', 'Type', 'string', True),
            ('valid', 'Geldig', 'boolean', True),
        ],
        "filters": [
            ('changed', 'beperk tot afspraken met wijzigingen', 'boolean'),
            ('includeHidden', 'vraag ook verwijderde afspraakversies op', 'boolean'),
            ('modifiedSince', 'beperk tot afspraakversies met een wijziging (inclusief leerlingdeelname) sinds het opgegeven moment', 'timestamp'),
            ('schoolInSchoolYear', 'afspraken in de opgegeven roosterprojecten', 'long'),
        ],
    },
    'branchesofschools': {
        "title": 'Vestigingen in project',
        "fields": [
            ('branch', 'Vestiging', 'string', True),
            ('id', 'ID', 'long', True),
            ('schoolInSchoolYear', 'Project', 'long', True),
        ],
        "filters": [
        ],
    },
    'branches': {
        "title": 'Vestigingen',
        "fields": [
            ('code', 'Vestigingscode', 'string', True),
            ('name', 'Naam', 'string', True),
            ('somCode', 'Exportcode LAS', 'string', True),
            ('somUuid', 'Somtoday Connect vestiging', 'uuid', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'vestigingen binnen de opgegeven roosterprojecten', 'long'),
        ],
    },
    'choosableindepartments': {
        "title": 'Vak-op-afdeling',
        "fields": [
            ('departmentOfBranch', 'Afdeling', 'long', True),
            ('id', 'ID', 'long', True),
            ('subject', 'Keuze', 'long', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot vak-op-afdelingen binnen een roosterproject', 'long'),
        ],
    },
    'contracts': {
        "title": 'Contracten',
        "fields": [
            ('employee', 'Werknemerscode', 'string', True),
            ('end', 'Eind', 'datum', True),
            ('id', 'ID', 'long', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('start', 'Start', 'datum', True),
        ],
        "filters": [
        ],
    },
    'courses': {
        "title": 'Lesgroepen',
        "fields": [
            ('branchCode', 'Vestiging', 'string', True),
            ('choosableInDepartment', 'Vak op afdeling', 'long', False),
            ('departmentCode', 'Afdeling', 'string', True),
            ('educationTypes', 'Opleidingstypes', 'string[]', False),
            ('groupName', 'Groepsnaam', 'string', False),
            ('id', 'ID', 'long', True),
            ('iltCode', 'Elementcode', 'integer', False),
            ('schoolYear', 'Schooljaar', 'integer', True),
            ('students', 'Leerlingen', 'json[]', False),
            ('subjectCode', 'Vakcode', 'string', False),
            ('subjectName', 'Vaknaam', 'string', False),
            ('teachers', 'Docenten', 'json[]', False),
            ('yearOfEducation', 'Leerjaar', 'integer', False),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot lesgroepen binnen een roosterproject', 'long'),
            ('student', 'beperk tot lesgroepen van een leerling', 'string'),
            ('teacher', 'beperk tot lesgroepen van een docent', 'string'),
        ],
    },
    'departmentsofbranches': {
        "title": 'Afdelingen',
        "fields": [
            ('branchOfSchool', 'Vestiging', 'long', True),
            ('code', 'Code / naam', 'string', True),
            ('id', 'ID', 'long', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
        ],
        "filters": [
        ],
    },
    'employeeabsences': {
        "title": 'Afwezigheden',
        "fields": [
            ('id', 'Id', 'long', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'afwezigheden binnen de opgegeven roosterprojecten', 'long'),
        ],
    },
    'employees': {
        "title": 'Werknemers',
        "fields": [
            ('commencementSchool', 'Op school vanaf', 'datum', True),
            ('commencementTeaching', 'Docent vanaf', 'datum', True),
            ('created', 'Aangemaakt', 'timestamp', True),
            ('email', 'Email', 'string', False),
            ('employeeNumber', 'Personeelsnummer', 'string', True),
            ('firstName', 'Voornaam', 'string', False),
            ('lastModified', 'Laatst gewijzigd', 'timestamp', True),
            ('lastModifiedBy', 'Laatst gewijzigd door', 'string', True),
            ('lastName', 'Achternaam', 'string', False),
            ('prefix', 'Tussenvoegsel', 'string', False),
            ('userCode', 'Gebruiker', 'string', True),
        ],
        "filters": [
            ('branchOfSchool', 'beperk tot werknemers gerelateerd aan een vestiging binnen een roosterproject', 'long'),
            ('schoolInSchoolYear', 'beperk tot werknemers gerelateerd aan een roosterproject', 'long'),
        ],
    },
    'enrollmentstatuspersubject': {
        "title": 'Inschrijfstatussen per vak',
        "fields": [
            ('choosableInDepartment', 'Vak-op-afdeling', 'long', True),
            ('plannedOptionalLessonAttendance', 'Geplande aanwezigheid optionele lessen', 'integer', True),
            ('plannedOptionalLessons', 'Aangeboden optionele lessen', 'integer', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('student', 'Leerling', 'string', True),
            ('week', 'Week', 'week', True),
        ],
        "filters": [
        ],
    },
    'enrollmentstatus': {
        "title": 'Inschrijfstatussen',
        "fields": [
            ('lessonEnrollment', 'Aantal inschrijvingen voor lessen', 'integer', True),
            ('maximalLessonEnrollment', 'Maximaal aantal inschrijvingen voor lessen per week', 'integer', True),
            ('minimalLessonEnrollment', 'Minimaal aantal inschrijvingen voor lessen per week', 'integer', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('student', 'Leerling', 'string', True),
            ('week', 'Week', 'week', True),
        ],
        "filters": [
        ],
    },
    'familymembers': {
        "title": 'Ouders/verzorgers',
        "fields": [
            ('email', 'Email', 'string', False),
            ('firstName', 'Voornaam', 'string', False),
            ('lastName', 'Achternaam', 'string', False),
            ('prefix', 'Tussenvoegsel', 'string', False),
            ('students', 'Kinderen', 'string[]', True),
            ('userCode', 'Gebruiker', 'string', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot ouders met een kind dat deelneemt aan een roosterproject', 'long'),
        ],
    },
    'groupindepartments': {
        "title": 'Roostergroepen',
        "fields": [
            ('id', 'id', 'long', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot roostergroepen binnen een roosterproject', 'long'),
        ],
    },
    'holidays': {
        "title": 'Vakanties',
        "fields": [
            ('end', 'Eind', 'datum', True),
            ('id', 'ID', 'long', True),
            ('name', 'Naam', 'string', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('start', 'Start', 'datum', True),
        ],
        "filters": [
        ],
    },
    'jobs': {
        "title": 'Aanstellingen',
        "fields": [
            ('contract', 'Werknemerscode', 'long', True),
            ('created', 'Aangemaakt', 'timestamp', True),
            ('durationManually', 'Duur handmatig?', 'boolean', True),
            ('employmentType', 'Dienstverband', 'string', False),
            ('end', 'Eind', 'datum', True),
            ('fte', 'WTF jaarequivalent', 'float', True),
            ('fteReal', 'WTF', 'float', True),
            ('functionCategory', 'Functiecategorie', 'string', False),
            ('id', 'id', 'long', True),
            ('lastModified', 'Laatst gewijzigd', 'timestamp', True),
            ('lastModifiedBy', 'Laatst gewijzigd door', 'string', True),
            ('start', 'Start', 'datum', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'aanstellingen binnen de opgegeven roosterprojecten', 'long'),
        ],
    },
    'liveschedule': {
        "title": 'Liverooster afspraken',
        "fields": [
            ('appointments', 'Roosterintervallen', 'json[]', False),
            ('replacements', 'Vervangingen', 'json[]', False),
            ('status', 'Weekstatussen', 'json[]', False),
            ('user', 'Gebruiker', 'string', False),
            ('week', 'Week', 'week', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'liverooster van een deelnemer aan een van de opgegeven roosterprojecten', 'long'),
            ('student', 'liverooster van de opgegeven leerling', 'string'),
            ('teacher', 'liverooster van de opgegeven docent', 'string'),
        ],
    },
    'locationofbranches': {
        "title": 'Lokalen',
        "fields": [
            ('branchOfSchool', 'Hoofdvestiging', 'integer', True),
            ('id', 'ID', 'long', True),
            ('name', 'Naam', 'string', True),
            ('schoolInSchoolYear', 'Roosterproject', 'integer', True),
        ],
        "filters": [
        ],
    },
    'parentteachernights': {
        "title": 'Ouderavonden',
        "fields": [
            ('allowRequestingUntil', 'Aanvragen toestaan tot', 'timestamp', True),
            ('archived', 'Gearchiveerd?', 'boolean', True),
            ('description', 'Nadere toelichting', 'string', True),
            ('hasParentToSchedulerRemark', 'Opmerking aan de roostermaker?', 'boolean', True),
            ('hasParentToTeacherRemark', 'Opmerking aan de docent?', 'boolean', True),
            ('maxNumberOfRequests', 'Maximaal aantal aanvragen per kind', 'integer', True),
            ('parentCanRequestLongTalk', 'Lang gesprek aanvraagbaar door ouders?', 'boolean', True),
            ('published', 'Gepubliceerd?', 'boolean', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('title', 'Naam', 'string', True),
        ],
        "filters": [
            ('familyMember', 'beperk tot ouderavonden met gesprekken van de opgegeven ouder', 'long[]'),
        ],
    },
    'parenttoschedulerremarks': {
        "title": 'Ouderavond opmerkingen van ouders',
        "fields": [
            ('familyMember', 'Ouder', 'string', True),
            ('id', 'ID', 'long', True),
            ('parentTeacherNight', 'Ouderavond', 'long', True),
            ('remark', 'Opmerking', 'string', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
        ],
        "filters": [
        ],
    },
    'schoolsinschoolyears': {
        "title": 'Roosterprojecten',
        "fields": [
            ('archived', 'Gearchiveerd', 'boolean', True),
            ('archivedTime', 'Archieftijd', 'timestamp', True),
            ('id', 'ID', 'long', True),
            ('name', 'Roosterproject Portal', 'string', False),
            ('school', 'School', 'long', True),
            ('year', 'Schooljaar', 'integer', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot het opgegeven roosterproject', 'long'),
        ],
    },
    'sectionassignments': {
        "title": 'Sectietoekenningen',
        "fields": [
            ('contract', 'Contract', 'long', True),
            ('id', 'ID', 'long', True),
            ('lessonHoursFirstDegree', 'Te plannen lessen 1e graads', 'float', True),
            ('lessonHoursSecondDegree', 'Te plannen lessen 2e graads', 'float', True),
            ('sectionOfBranch', 'Sectie', 'long', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot sectietoekenningen binnen een roosterproject', 'long'),
        ],
    },
    'sectionofbranches': {
        "title": 'Sectie-activaties',
        "fields": [
            ('branchOfSchool', 'Vestiging-in-project', 'long', True),
            ('id', 'ID', 'long', True),
            ('section', 'Sectie', 'long', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot sectie-activaties binnen een roosterproject', 'long'),
        ],
    },
    'sections': {
        "title": 'Secties',
        "fields": [
            ('abbreviation', 'Afkorting', 'string', True),
            ('id', 'ID', 'long', True),
            ('name', 'Naam sectie', 'string', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot secties geactiveerd binnen een roosterproject', 'long'),
        ],
    },
    'standardprognosis': {
        "title": 'Standaardprognoses',
        "fields": [
            ('id', 'ID', 'long', True),
            ('percentage', 'Percentage', 'integer', True),
            ('sourceDepartment', 'Bronafdeling', 'long', True),
            ('targetDepartment', 'Doelafdeling', 'long', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot standaardprognoses met het opgegeven project als bron of doel', 'long'),
        ],
    },
    'studentsindepartments': {
        "title": 'Afdelingsdeelnames',
        "fields": [
            ('id', 'Id', 'long', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('student', 'Leerlingcode', 'string', True),
        ],
        "filters": [
            ('archived', 'beperk tot afdelingsdeelnames van actieve of gearchiveerde leerlingen', 'boolean'),
            ('branchOfSchool', 'beperk tot afdelingsdeelnames binnen een vestiging', 'long'),
        ],
    },
    'students': {
        "title": 'Leerlingen',
        "fields": [
            ('email', 'Email', 'string', False),
            ('familyMembers', 'Ouders', 'string[]', True),
            ('firstName', 'Voornaam', 'string', False),
            ('lastName', 'Achternaam', 'string', False),
            ('prefix', 'Tussenvoegsel', 'string', False),
            ('userCode', 'Leerlingcode', 'string', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot leerlingen binnen een roosterproject', 'long[]'),
        ],
    },
    'subjectselectionsubjects': {
        "title": 'Keuzes',
        "fields": [
            ('code', 'Keuzecode', 'string', True),
            ('id', 'ID', 'long', True),
            ('iltCode', 'Elementcode', 'string', True),
            ('name', 'Naam', 'string', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'beperk tot keuze-objecten (vakken/profielen/opleidingen) binnen een roosterproject', 'long'),
        ],
    },
    'talkdays': {
        "title": 'Ouderavonddagen',
        "fields": [
            ('date', 'Datum', 'datum', True),
            ('id', 'ID', 'long', True),
            ('parentTeacherNight', 'Ouderavond', 'long', True),
            ('title', 'Naam', 'string', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'Ouderavonddagen binnen de opgegeven roosterprojecten', 'long'),
        ],
    },
    'talkrequests': {
        "title": 'Ouderavondgespreksaanvragen',
        "fields": [
            ('appointment', 'Afspraak', 'long', True),
            ('employees', 'Docentcodes', 'string[]', True),
            ('extended', 'Gewenst aantal tijdslots', 'long', True),
            ('familyMembers', 'Ouders', 'string[]', True),
            ('id', 'ID', 'long', True),
            ('parentTeacherNight', 'Ouderavond', 'long', True),
            ('parentToTeacherRemark', 'Opmerking van ouders voor docent', 'string', True),
            ('requested', 'Aangevraagd', 'boolean', True),
            ('schedulerToParentRemark', 'Opmerking van roostermaker voor ouders', 'string', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('student', 'Leerlingnummer', 'string', True),
            ('table', 'Tafel', 'string', True),
            ('talkTimeSlot', 'Tijdslot', 'long', True),
            ('title', 'Onderwerp', 'string', True),
        ],
        "filters": [
            ('familyMemberSomUUID', 'beperk tot gespreksaanvragen voor de (met Somtoday UUID) opgegeven ouder', 'uuid'),
        ],
    },
    'talktimeblockabsenceparent': {
        "title": 'Ouderavond ouder-moment verhinderingen',
        "fields": [
            ('id', 'ID', 'long', True),
            ('schoolInSchoolYear', 'Roosterproject', 'long', True),
            ('talkDay', 'Gespreksdag', 'long', True),
            ('talkTimeBlock', 'Gesprekstijdverzameling', 'long', True),
            ('user', 'Gebruiker', 'string', True),
        ],
        "filters": [
            ('parentTeacherNight', 'verhinderingen binnen de opgegeven ouderavonden', 'long'),
        ],
    },
    'talktimeblocks': {
        "title": 'Ouderavond gesprekstijdverzamelingen',
        "fields": [
            ('id', 'ID', 'long', True),
            ('parentTeacherNight', 'Ouderavond', 'long', True),
            ('span', 'Totale tijdsbereik gesprekverzamelingen', 'string', False),
            ('talkTimeSlots', 'Gesprekstijden', 'long[]', True),
            ('title', 'Naam', 'string', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'gesprekstijdverzamelingen binnen de opgegeven roosterprojecten', 'long'),
        ],
    },
    'timeslotnames': {
        "title": 'Lesuurnamen',
        "fields": [
            ('code', 'Code', 'string', True),
            ('id', 'ID', 'long', True),
            ('schoolInSchoolYear', 'Project', 'long', True),
        ],
        "filters": [
        ],
    },
    'users': {
        "title": 'Gebruikers',
        "fields": [
            ('code', 'Gebruikerscode', 'string', True),
            ('email', 'Email', 'string', True),
            ('firstName', 'Voornaam', 'string', True),
            ('lastName', 'Achternaam', 'string', True),
            ('magisterUUID', 'Magister UUID', 'uuid', True),
            ('prefix', 'Tussenvoegsel', 'string', True),
            ('somUUID', 'Somtoday UUID', 'uuid', True),
        ],
        "filters": [
            ('schoolInSchoolYear', 'gebruikers verbonden aan de opgegeven roosterprojecten', 'long'),
        ],
    },
}
