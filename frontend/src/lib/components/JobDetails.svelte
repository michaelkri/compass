<script lang="ts">
    let { id, title, company, location, source, url, description, jobs } = $props();

    async function deleteJob() {
        const url = "http://localhost:8000/api/jobs/";

        try {
            const response = await fetch(url + id, {
                method: "DELETE",
            });

            if (response.status === 204) {
                jobs = jobs.filter((job: { id: number }) => job.id != id);
            } else {
                console.log(response.status);
            }
        } catch (error) {
            console.error(error);
        }
    }
</script>

<div id="job-details" class="mx-auto max-w-3xl">
    <div class="border-border mb-8 border-b pb-6 dark:border-gray-200">
        <div class="mb-4 flex items-start justify-between gap-4">
            <h1 class="job-title text-foreground flex-1 text-2xl font-bold">
                {title}
            </h1>
            <button
                class="p-2 cursor-pointer rounded-md hover:bg-gray-200 dark:hover:bg-gray-950"
                aria-label="Delete Job"
                onclick={() => deleteJob()}
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-5 w-5 lucide lucide-trash2-icon lucide-trash-2"
                    ><path d="M10 11v6" /><path d="M14 11v6" /><path
                        d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"
                    /><path d="M3 6h18" /><path
                        d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                    /></svg
                >
            </button>
        </div>
        <div
            class="text-muted-foreground mb-4 flex flex-wrap items-center gap-3 text-sm"
        >
            <span class="job-company">{company}</span><span>•</span>
            <div class="job-location flex items-center gap-1.5">
                <span>{location}</span>
            </div>
            <span
                class="job-source border-border rounded-md border px-2 py-0.5 text-xs"
                >{source}</span
            >
        </div>
        <a
            target="_blank"
            rel="noopener noreferrer"
            href={url}
            class="job-url-button text-white bg-slate-900 hover:bg-slate-800 focus:ring-4 focus:outline-none focus:ring-[#050708]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center me-2 mb-2"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="w-4 h-4 me-2 -ms-1 lucide lucide-external-link-icon lucide-external-link"
            >
                <path d="M15 3h6v6" />
                <path d="M10 14 21 3" />
                <path
                    d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
                />
            </svg>
            <span class="font-semibold">View Source</span>
        </a>
    </div>
    <div class="job-description prose max-w-none dark:text-gray-200">
        <p>{@html description}</p>
    </div>
</div>
