export function GoldMSI(options = {}) {
    const defaultSurveyJson = {
        showQuestionNumbers: false,
        elements: [
            {
                type: "matrix",
                name: "general_msi",
                title: "Please rate your agreement with the following statements:",
                columns: [
                    { value: 1, text: "1 - Completely Disagree" },
                    { value: 2, text: "2 - Strongly Disagree" },
                    { value: 3, text: "3 - Disagree" },
                    { value: 4, text: "4 - Neither Agree nor Disagree" },
                    { value: 5, text: "5 - Agree" },
                    { value: 6, text: "6 - Strongly Agree" },
                    { value: 7, text: "7 - Completely Agree" },
                ],
                rows: [
                    { value: "free_time", text: "I spend a lot of my free time doing music-related activities." },
                    { value: "writing", text: "I enjoy writing about music, for example on blogs and forums." },
                    { value: "join_in", text: "If somebody starts singing a song I don't know, I can usually join in." },
                    { value: "memory", text: "I can sing or play music from memory." },
                    { value: "accuracy", text: "I am able to hit the right notes when I sing along with a recording." },
                    { value: "compare", text: "I can compare and discuss differences between two performances or versions of the same piece of music." },
                    { value: "compliment", text: "I have never been complimented for my talents as a musical performer." },
                    { value: "reading", text: "I often read or search the internet for things related to music." },
                    { value: "harmony", text: "I am not able to sing in harmony when somebody is singing a familiar tune." },
                    { value: "special", text: "I am able to identify what is special about a given musical piece." },
                    { value: "in_tune", text: "When I sing, I have no idea whether I'm in tune or not." },
                    { value: "addiction", text: "Music is kind of an addiction for me—I couldn't live without it." },
                    { value: "public", text: "I don't like singing in public because I'm afraid that I would sing wrong notes." },
                    { value: "musician", text: "I would not consider myself a musician." },
                    { value: "myself", text: "After hearing a new song two or three times, I can usually sing it by myself." },
                    { value: "musical_theatre", text: "I am a big fan of musicals." },
                ],
                isAllRowRequired: true,
            },
        ],
    };

    return {
        type: jsPsychSurvey,
        css_classes: ["general-msi"],
        no_load_css: true,
        min_width: "1200px",
        ...options,
        survey_json: {
            ...defaultSurveyJson,
            ...(options.survey_json || {}),
        },
    };
}

// Example usage inside a future experiment:
// import { GoldMSI } from "{{ url_for('static', filename='js/Gold-MSI.js') }}";
// timeline.push(GoldMSI());
