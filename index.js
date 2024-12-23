// import 'dotenv/config';
import { youtube_v3 } from '@googleapis/youtube';
import { generateOneVideoRec } from './portal-lib.js';

// Your API key
// const API_KEY = process.env.YOUTUBE_API_KEY; // Load API key from .env file
//
// // Function to generate random dates between 2008 and 2010
// function generateRandomDate() {
//     const startYear = 2008;
//     const endYear = 2010;
//
//     const startDate = new Date(startYear, 0, 1).getTime();
//     const endDate = new Date(endYear, 11, 31).getTime();
//
//     const randomTimestamp = Math.floor(Math.random() * (endDate - startDate + 1)) + startDate;
//     return new Date(randomTimestamp);
// }
//
// // Function to add days to a date
// function addDaysToDate(date, days) {
//     const newDate = new Date(date);
//     newDate.setDate(newDate.getDate() + days);
//     return newDate;
// }
//
// // Function to search for videos with 'IMG' in the title
// async function searchVideosWithIMG() {
//     let publishedAfter = generateRandomDate();
//     let publishedBefore = addDaysToDate(publishedAfter, 3);
//
//     console.log(publishedBefore.toUTCString() + "\n---");
//
//     try {
//         const youtube = new youtube_v3.Youtube({
//             auth: API_KEY,
//         });
//
//         const response = await youtube.search.list({
//             part: 'snippet',
//             q: 'IMG .mov',
//             type: 'video',
//             publishedBefore: publishedBefore.toISOString(),
//             publishedAfter: publishedAfter.toISOString(),
//             maxResults: 10,
//         });
//
//         const filteredVideos = response.data.items.filter((item) => {
//             const title = item.snippet.title.toLowerCase();
//             return true//title.includes('img') && (title.includes('.mov') || title.includes('mov'));
//         });
//
//         filteredVideos.forEach(video => {
//             console.log(`Title: ${video.snippet.title}`);
//             console.log(`Video ID: ${video.id.videoId}`);
//             console.log(`Video Desc.: ${video.snippet.description}`);
//             console.log(`Video Link: https://www.youtube.com/watch?v=${video.id.videoId}`);
//             console.log('---');
//         });
//
//         return filteredVideos;
//     } catch (error) {
//         console.error('Error fetching videos:', error);
//     }
// }

// Call the function
// searchVideosWithIMG()
generateOneVideoRec().then(videos => {
    videos.forEach(video => {
        console.log(`Title: ${video.snippet.title}`);
        console.log(`Video ID: ${video.id.videoId}`);
        console.log(`Video Desc.: ${video.snippet.description}`);
        console.log(`Video Link: https://www.youtube.com/watch?v=${video.id.videoId}`);
        console.log('---');
    });
});
