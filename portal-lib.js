import 'dotenv/config';
import { youtube_v3 } from '@googleapis/youtube';

// Your API key
const API_KEY = process.env.YOUTUBE_API_KEY; // Load API key from .env file


// Function to generate random dates between 2008 and 2010
function generateRandomDate() {
    const startYear = 2008;
    const endYear = 2010;

    const startDate = new Date(startYear, 0, 1).getTime();
    const endDate = new Date(endYear, 11, 31).getTime();

    const randomTimestamp = Math.floor(Math.random() * (endDate - startDate + 1)) + startDate;
    return new Date(randomTimestamp);
}

// Function to add days to a date
function addDaysToDate(date, days) {
    const newDate = new Date(date);
    newDate.setDate(newDate.getDate() + days);
    return newDate;
}

// Recursive function to fetch one video
async function generateOneVideoRec() {
    const q = 'IMG .mov';
    const qty = 1;
    let publishedBefore = generateRandomDate();
    let publishedAfter = addDaysToDate(publishedBefore, 1);

    console.log("Probing date: " + publishedBefore.toISOString() + "\n")


    let videos = await searchVideosWithIMG(
        q,
        qty,
        publishedAfter,
        publishedBefore,
        null,
        null
    );

    return videos; //todo: if empty than switch date and try again
    // if(!videos){
    //     return videos; /// error
    // } else if (videos.length === 0) {
    //     return videos;// return await generateOneVideoRec();
    // } else {
    //     return videos;
    // }
}

// Function to search for videos with IMG in the title
async function searchVideosWithIMG(queryString, qtyResults, before, after, location, radius) {
    try {
        const youtube = new youtube_v3.Youtube({
            auth: API_KEY,
        });

        const response = await youtube.search.list({
            part: 'snippet',
            q: queryString,
            type: 'video',
            publishedBefore: before.toISOString(),
            publishedAfter: after.toISOString(),
            maxResults: qtyResults,
            // location: location,
            // locationRadius: radius
        });

        // Filter results for case-insensitive "IMG" and ".mov" or "mov"
        const filteredVideos = response.data.items.filter((item) => {
            const title = item.snippet.title.toLowerCase();
            return true//title.includes('img') && (title.includes('.mov') || title.includes('mov'));
        });

        return filteredVideos;
    } catch (error) {
        console.error('Error fetching videos:', error);
    }
}

export { generateOneVideoRec };
