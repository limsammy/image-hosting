/**
 * Gallery Page
 * Visual-only proof of concept matching the Stitch design mockup
 */

// Mock data for gallery items
const mockImages = [
  { id: 1, filename: 'mountain_view_01.jpg', addedAgo: '2 mins ago' },
  { id: 2, filename: 'lake_retreat.png', addedAgo: '45 mins ago' },
  { id: 3, filename: 'forest_hike_2024.webp', addedAgo: '3 hours ago' },
  { id: 4, filename: 'ocean_aerial.jpg', addedAgo: '1 day ago' },
  { id: 5, filename: 'everest_peak.jpeg', addedAgo: '2 days ago' },
  { id: 6, filename: 'san_fran_bridge.jpg', addedAgo: '3 days ago' },
  { id: 7, filename: 'grand_canyon.png', addedAgo: '4 days ago' },
  { id: 8, filename: 'aurora_borealis.jpg', addedAgo: '5 days ago' },
];

// Placeholder colors for image thumbnails
const placeholderColors = [
  'bg-indigo-200 dark:bg-indigo-900',
  'bg-teal-200 dark:bg-teal-900',
  'bg-emerald-200 dark:bg-emerald-900',
  'bg-cyan-200 dark:bg-cyan-900',
  'bg-violet-200 dark:bg-violet-900',
  'bg-rose-200 dark:bg-rose-900',
  'bg-orange-200 dark:bg-orange-900',
  'bg-slate-200 dark:bg-slate-800',
];

export default function Gallery() {
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary">
      {/* Navigation Bar */}
      <header className="sticky top-0 z-50 w-full bg-surface-primary border-b border-border-primary">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h1 className="text-xl font-semibold tracking-tight">Image Host</h1>
            </div>

            {/* User Info & Actions */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex flex-col items-end">
                <span className="text-sm font-semibold">johndoe</span>
                <span className="text-xs text-primary font-medium">Pro Account</span>
              </div>
              <button className="btn-secondary btn-sm">Account</button>
              <a href="/login" className="btn-primary btn-sm">Logout</a>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Section */}
        <section className="mb-12">
          <div className="dropzone py-16 hover:border-primary/50 hover:bg-primary-50/50 dark:hover:bg-primary-900/10">
            <div className="flex flex-col items-center gap-4">
              {/* Cloud Upload Icon */}
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <svg className="w-8 h-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z" />
                </svg>
              </div>
              <div className="text-center">
                <p className="heading-5 mb-1">Drag and drop images here</p>
                <p className="body-sm text-text-tertiary">Support for JPG, PNG, WEBP up to 10MB</p>
              </div>
            </div>
            <button className="btn-primary mt-6">Choose Files</button>
          </div>
        </section>

        {/* Gallery Header */}
        <div className="flex items-center justify-between mb-6 px-1">
          <h2 className="heading-4">Your Gallery</h2>
          <span className="body-sm text-text-tertiary">Showing 8 of 156 images</span>
        </div>

        {/* Image Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          {mockImages.map((image, index) => (
            <GalleryItem
              key={image.id}
              filename={image.filename}
              addedAgo={image.addedAgo}
              colorClass={placeholderColors[index % placeholderColors.length]}
              faded={index >= 6}
            />
          ))}
        </div>

        {/* Load More Button */}
        <div className="flex justify-center mt-12 mb-8">
          <button className="btn-outline h-12 px-8">
            Load More Images
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-border-primary py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            {/* Logo & Copyright */}
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-primary/10 rounded flex items-center justify-center">
                <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <span className="body-sm text-text-tertiary">© 2024 Image Host Inc.</span>
            </div>

            {/* Footer Links */}
            <div className="flex gap-8">
              <a href="#" className="body-sm text-text-tertiary hover:text-text-primary transition-colors">API Documentation</a>
              <a href="#" className="body-sm text-text-tertiary hover:text-text-primary transition-colors">Terms of Service</a>
              <a href="#" className="body-sm text-text-tertiary hover:text-text-primary transition-colors">Privacy Policy</a>
              <a href="#" className="body-sm text-text-tertiary hover:text-text-primary transition-colors">Help Center</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Gallery Item Component
function GalleryItem({
  filename,
  addedAgo,
  colorClass,
  faded = false,
}: {
  filename: string;
  addedAgo: string;
  colorClass: string;
  faded?: boolean;
}) {
  return (
    <div className={`group card-interactive overflow-hidden ${faded ? 'opacity-60' : ''}`}>
      {/* Image Placeholder */}
      <div className="relative aspect-square w-full overflow-hidden">
        <div
          className={`w-full h-full ${colorClass} flex items-center justify-center transition-transform duration-300 group-hover:scale-105`}
        >
          <svg className="w-12 h-12 text-current opacity-30" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>

      {/* Card Content */}
      <div className="p-4">
        <p className="text-sm font-semibold truncate mb-1">{filename}</p>
        <p className="caption mb-4">Added {addedAgo}</p>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button className="flex-1 flex items-center justify-center gap-2 rounded-lg h-9 px-3 bg-primary/10 text-primary text-xs font-semibold hover:bg-primary/20 transition-colors">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            <span>URL</span>
          </button>
          <button className="flex items-center justify-center rounded-lg h-9 w-9 bg-error-50 text-error-600 hover:bg-error-100 dark:bg-error-900/20 dark:text-error-400 dark:hover:bg-error-900/30 transition-colors">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
