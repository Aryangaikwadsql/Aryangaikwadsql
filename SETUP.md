# Profile README setup

This profile uses a repository named after your GitHub username. The README links and
the snake image currently use `Aryangaikwadsql`; update those URLs if the profile
repository is published under a different username.

## Enable the contribution calendar

1. Make the profile repository public.
2. In **Settings → Actions → General → Workflow permissions**, enable **Read and write
   permissions**.
3. Create a GitHub personal access token with `read:user` access. Add it to this
   repository under **Settings → Secrets and variables → Actions** as `METRICS_TOKEN`.
4. Enable Actions if prompted, then manually run the **Metrics** and **Snake**
   workflows once.

The Metrics workflow refreshes `assets/metrics.isocalendar.svg` every six hours. The
Snake workflow publishes light and dark snake animations to the `output` branch every
twelve hours. The snake images may not appear until the first workflow run finishes.
