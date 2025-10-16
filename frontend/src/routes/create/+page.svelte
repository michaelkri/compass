<script>
    let data = $state({
        id: 0,
        title: "",
        company: "",
        location: "",
        source: "",
        url: "",
        description: ""
    });

    async function submitJob() {
        const response = await fetch("http://localhost:8000/api/job/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server responded with validation errors:", errorData);
            throw new Error("Request failed with status " + response.status);
        }

        const responseData = await response.json();
        console.log(responseData)
    }
</script>

<section class="bg-white dark:bg-gray-900">
    <div class="py-8 px-4 mx-auto max-w-2xl lg:py-16">
        <div class="mb-4">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                Add a new job
            </h2>
            <span class="text-gray-700"
                >Use this page to add custom jobs which weren't scraped
                automatically.</span
            >
        </div>
        <form action="#">
            <div class="grid gap-4 sm:grid-cols-2 sm:gap-6">
                <div class="sm:col-span-2">
                    <label
                        for="title"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >Job title</label
                    >
                    <input
                        type="text"
                        name="title"
                        id="title"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                        placeholder="Job title"
                        bind:value={data.title}
                    />
                </div>
                <div class="w-full">
                    <label
                        for="company"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >Company</label
                    >
                    <input
                        type="text"
                        name="company"
                        id="company"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                        placeholder="Company"
                        bind:value={data.company}
                    />
                </div>
                <div class="w-full">
                    <label
                        for="location"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >Location</label
                    >
                    <input
                        type="text"
                        name="location"
                        id="location"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                        placeholder="City"
                        bind:value={data.location}
                    />
                </div>
                <div>
                    <label
                        for="source"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >Source</label
                    >
                    <select
                        id="source"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                        bind:value={data.source}
                    >
                        <option value="Indeed">Indeed</option>
                        <option value="LinkedIn">LinkedIn</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div>
                    <label
                        for="url"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >URL</label
                    >
                    <input
                        type="url"
                        name="url"
                        id="url"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                        placeholder="https://il.indeed.com/viewjob?jk=..."
                        bind:value={data.url}
                    />
                </div>
                <div class="sm:col-span-2">
                    <label
                        for="description"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                        >Description</label
                    >
                    <textarea
                        id="description"
                        rows="8"
                        class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                        placeholder="Job description"
                        bind:value={data.description}
                    ></textarea>
                </div>
            </div>
            <button
                type="submit"
                class="inline-flex items-center px-5 py-2.5 mt-4 sm:mt-6 text-sm font-medium text-center text-white bg-blue-500 rounded-lg cursor-pointer hover:bg-blue-800"
                onclick={submitJob}
            >
                Add Job
            </button>
        </form>
    </div>
</section>
