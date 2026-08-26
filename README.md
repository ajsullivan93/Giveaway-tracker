# Giveaway Tracker
A GitHub Pages-ready PWA that tracks sweepstakes and refreshes a discovery queue daily.

## Install
1. Create a GitHub repository and upload this folder.
2. Enable GitHub Pages for the repository.
3. Open the Pages URL in iPhone Safari.
4. Share → Add to Home Screen.

## Daily discovery
GitHub Actions runs `sync_giveaways.py` daily. The sync is deliberately conservative: it preserves curated records and adds candidates from Sweepstakes Radar, Sweepstakes Fanatics and SweepstakesBible for review. It does not automatically enter sweepstakes.

## Safety
Always follow each sweepstakes' official rules. Some promotions prohibit automated or repeated submissions, and some directory entries may have limited-state eligibility.
