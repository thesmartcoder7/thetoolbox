export interface Repository {
    repository: {
        id: number;
        owner: string;
        name: string;
        url: string;
    };
    overall_score: number;
    analysis_results: {
        category: string;
        score: number;
        details: {
            description: string;
            recommendations: {
                text: string;
                link: string;
            }[];
            [key: string]: any; // Allows additional dynamic properties like has_installation, has_wiki, etc.
        };
    }[];
}
