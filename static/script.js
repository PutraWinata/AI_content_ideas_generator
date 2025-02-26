function generateContent() {
    const goal = document.getElementById("goal").value;
    const platform = document.getElementById("platform").value;
    const contentType = document.getElementById("content_type").value;
    const targetAudience = document.getElementById("target_audience").value;
    const competitors = document.getElementById("competitors").value;
    const trends = document.getElementById("trends").value;

    fetch("/generate", {
        method: "POST",
        body: JSON.stringify({
            goal, platform, content_type: contentType, 
            target_audience: targetAudience, 
            competitors, trends
        }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        const responseContainer = document.getElementById("ai-response");
        responseContainer.innerHTML = ""; // Clear previous results
        document.getElementById("result").style.display = "block";

        // Split AI response into separate content ideas
        const contentIdeas = data.content_ideas.split("\n\n"); // Double line breaks for separation

        contentIdeas.forEach((idea) => {
            if (idea.trim() !== "") {
                // Create a list item for each content idea
                const listItem = document.createElement("li");

                // Format text: Bold subtitles, line breaks, and structure
                listItem.innerHTML = idea
                    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Convert **bold** to HTML <strong>
                    .replace(/\n/g, "<br>"); // Add line breaks for better readability
                
                responseContainer.appendChild(listItem);
            }
        });
    })
    .catch(error => console.error("Error:", error));
}
