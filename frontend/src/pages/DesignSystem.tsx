import { useState } from 'react';

type Theme = 'default' | 'teal' | 'violet' | 'emerald' | 'rose' | 'orange' | 'cyan' | 'slate';

const themes: Theme[] = ['default', 'teal', 'violet', 'emerald', 'rose', 'orange', 'cyan', 'slate'];

const colorShades = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900', '950'] as const;
const palettes = ['indigo', 'teal', 'violet', 'emerald', 'rose', 'slate', 'orange', 'cyan'] as const;

function ColorSwatch({ color, label }: { color: string; label: string }) {
  return (
    <div className="flex flex-col items-center gap-1">
      <div
        className="w-12 h-12 rounded-lg shadow-sm border border-border-primary"
        style={{ backgroundColor: `var(--color-${color})` }}
      />
      <span className="text-xs text-text-tertiary">{label}</span>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-16">
      <h2 className="heading-2 mb-8 pb-4 border-b border-border-primary">{title}</h2>
      {children}
    </section>
  );
}

function SubSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-8">
      <h3 className="heading-5 mb-4 text-text-secondary">{title}</h3>
      {children}
    </div>
  );
}

export default function DesignSystem() {
  const [theme, setTheme] = useState<Theme>('default');
  const [isDark, setIsDark] = useState(false);

  const themeClass = theme === 'default' ? '' : `theme-${theme}`;
  const darkClass = isDark ? 'dark' : '';

  return (
    <div className={`min-h-screen ${themeClass} ${darkClass}`}>
      <div className="bg-bg-primary text-text-primary transition-colors duration-slow">
        {/* Header */}
        <header className="sticky top-0 z-sticky bg-surface-elevated border-b border-border-primary shadow-sm">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <h1 className="heading-4">Design System</h1>
            <div className="flex items-center gap-4">
              {/* Theme Selector */}
              <select
                value={theme}
                onChange={(e) => setTheme(e.target.value as Theme)}
                className="select text-sm py-2"
              >
                {themes.map((t) => (
                  <option key={t} value={t}>
                    {t.charAt(0).toUpperCase() + t.slice(1)}
                  </option>
                ))}
              </select>
              {/* Dark Mode Toggle */}
              <button
                onClick={() => setIsDark(!isDark)}
                className="btn-outline btn-sm"
              >
                {isDark ? 'Light Mode' : 'Dark Mode'}
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-6xl mx-auto px-6 py-12">
          {/* Typography Section */}
          <Section title="Typography">
            <SubSection title="Headings (Thin Weights)">
              <div className="space-y-4">
                <p className="heading-display">Display - Font Thin</p>
                <p className="heading-1">Heading 1 - Extralight</p>
                <p className="heading-2">Heading 2 - Light</p>
                <p className="heading-3">Heading 3 - Light</p>
                <p className="heading-4">Heading 4 - Normal</p>
                <p className="heading-5">Heading 5 - Normal</p>
                <p className="heading-6">Heading 6 - Medium</p>
              </div>
            </SubSection>

            <SubSection title="Body Text">
              <div className="space-y-4 max-w-2xl">
                <p className="body-lg">
                  Body Large - The quick brown fox jumps over the lazy dog. This text demonstrates the large body style with light weight.
                </p>
                <p className="body-base">
                  Body Base - The quick brown fox jumps over the lazy dog. This is the default body text style for most content.
                </p>
                <p className="body-sm">
                  Body Small - The quick brown fox jumps over the lazy dog. Used for secondary content and compact layouts.
                </p>
                <p className="body-xs">
                  Body XS - The quick brown fox jumps over the lazy dog. Smallest body text for meta information.
                </p>
              </div>
            </SubSection>

            <SubSection title="Labels & Captions">
              <div className="space-y-2">
                <p className="label">Label Text - Form Labels</p>
                <p className="label-sm">Small Label - Secondary Labels</p>
                <p className="caption">Caption - Helper text and descriptions</p>
              </div>
            </SubSection>

            <SubSection title="Links">
              <div className="flex gap-6">
                <a href="#" className="link">Standard Link</a>
                <a href="#" className="link-subtle">Subtle Link</a>
              </div>
            </SubSection>

            <SubSection title="Font Weight Scale">
              <div className="grid grid-cols-7 gap-4">
                <div className="text-center">
                  <p className="text-2xl font-thin">Aa</p>
                  <p className="caption">Thin (100)</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-extralight">Aa</p>
                  <p className="caption">Extralight (200)</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-light">Aa</p>
                  <p className="caption">Light (300)</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-normal">Aa</p>
                  <p className="caption">Normal (400)</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-medium">Aa</p>
                  <p className="caption">Medium (500)</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-semibold">Aa</p>
                  <p className="caption">Semibold (600)</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold">Aa</p>
                  <p className="caption">Bold (700)</p>
                </div>
              </div>
            </SubSection>
          </Section>

          {/* Colors Section */}
          <Section title="Colors">
            <SubSection title="Primary Palette (Theme-Aware)">
              <div className="flex gap-2 flex-wrap">
                {colorShades.map((shade) => (
                  <ColorSwatch key={shade} color={`primary-${shade}`} label={shade} />
                ))}
              </div>
            </SubSection>

            <SubSection title="Semantic Colors">
              <div className="grid grid-cols-4 gap-8">
                <div>
                  <p className="label mb-2">Success</p>
                  <div className="flex gap-2">
                    <ColorSwatch color="success-50" label="50" />
                    <ColorSwatch color="success-500" label="500" />
                    <ColorSwatch color="success-700" label="700" />
                  </div>
                </div>
                <div>
                  <p className="label mb-2">Warning</p>
                  <div className="flex gap-2">
                    <ColorSwatch color="warning-50" label="50" />
                    <ColorSwatch color="warning-500" label="500" />
                    <ColorSwatch color="warning-700" label="700" />
                  </div>
                </div>
                <div>
                  <p className="label mb-2">Error</p>
                  <div className="flex gap-2">
                    <ColorSwatch color="error-50" label="50" />
                    <ColorSwatch color="error-500" label="500" />
                    <ColorSwatch color="error-700" label="700" />
                  </div>
                </div>
                <div>
                  <p className="label mb-2">Secondary</p>
                  <div className="flex gap-2">
                    <ColorSwatch color="secondary-100" label="100" />
                    <ColorSwatch color="secondary-500" label="500" />
                    <ColorSwatch color="secondary-900" label="900" />
                  </div>
                </div>
              </div>
            </SubSection>

            <SubSection title="All Color Palettes">
              <div className="space-y-6">
                {palettes.map((palette) => (
                  <div key={palette}>
                    <p className="label mb-2 capitalize">{palette}</p>
                    <div className="flex gap-1 flex-wrap">
                      {colorShades.map((shade) => (
                        <ColorSwatch key={shade} color={`${palette}-${shade}`} label={shade} />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </SubSection>
          </Section>

          {/* Buttons Section */}
          <Section title="Buttons">
            <SubSection title="Variants">
              <div className="flex flex-wrap gap-4 items-center">
                <button className="btn-primary">Primary</button>
                <button className="btn-secondary">Secondary</button>
                <button className="btn-outline">Outline</button>
                <button className="btn-ghost">Ghost</button>
                <button className="btn-danger">Danger</button>
              </div>
            </SubSection>

            <SubSection title="Sizes">
              <div className="flex flex-wrap gap-4 items-center">
                <button className="btn-primary btn-sm">Small</button>
                <button className="btn-primary">Default</button>
                <button className="btn-primary btn-lg">Large</button>
                <button className="btn-primary btn-xl">Extra Large</button>
              </div>
            </SubSection>

            <SubSection title="States">
              <div className="flex flex-wrap gap-4 items-center">
                <button className="btn-primary">Default</button>
                <button className="btn-primary" disabled>Disabled</button>
              </div>
            </SubSection>

            <SubSection title="Icon Buttons">
              <div className="flex flex-wrap gap-4 items-center">
                <button className="btn-icon btn-outline btn-icon-sm">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <button className="btn-icon btn-outline">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <button className="btn-icon btn-outline btn-icon-lg">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </button>
              </div>
            </SubSection>
          </Section>

          {/* Inputs Section */}
          <Section title="Form Inputs">
            <div className="max-w-md space-y-6">
              <SubSection title="Text Input">
                <div className="space-y-4">
                  <div>
                    <label className="label mb-1.5 block">Default Input</label>
                    <input type="text" className="input" placeholder="Enter text..." />
                  </div>
                  <div>
                    <label className="label mb-1.5 block">Small Input</label>
                    <input type="text" className="input input-sm" placeholder="Small input..." />
                  </div>
                  <div>
                    <label className="label mb-1.5 block">Large Input</label>
                    <input type="text" className="input input-lg" placeholder="Large input..." />
                  </div>
                  <div>
                    <label className="label mb-1.5 block">Error State</label>
                    <input type="text" className="input input-error" placeholder="Error input..." />
                    <p className="caption text-error-600 mt-1">This field has an error</p>
                  </div>
                  <div>
                    <label className="label mb-1.5 block">Disabled</label>
                    <input type="text" className="input" placeholder="Disabled input..." disabled />
                  </div>
                </div>
              </SubSection>

              <SubSection title="Textarea">
                <div>
                  <label className="label mb-1.5 block">Message</label>
                  <textarea className="textarea" placeholder="Write your message..." />
                </div>
              </SubSection>

              <SubSection title="Select">
                <div>
                  <label className="label mb-1.5 block">Choose an option</label>
                  <select className="select">
                    <option>Option 1</option>
                    <option>Option 2</option>
                    <option>Option 3</option>
                  </select>
                </div>
              </SubSection>

              <SubSection title="Checkbox & Radio">
                <div className="space-y-3">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" className="checkbox" />
                    <span className="body-sm">Checkbox option</span>
                  </label>
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input type="radio" name="radio" className="radio" />
                    <span className="body-sm">Radio option 1</span>
                  </label>
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input type="radio" name="radio" className="radio" />
                    <span className="body-sm">Radio option 2</span>
                  </label>
                </div>
              </SubSection>
            </div>
          </Section>

          {/* Cards Section */}
          <Section title="Cards">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="card">
                <div className="card-body">
                  <h3 className="heading-5 mb-2">Basic Card</h3>
                  <p className="body-sm">A simple card with border styling.</p>
                </div>
              </div>

              <div className="card-elevated">
                <div className="card-body">
                  <h3 className="heading-5 mb-2">Elevated Card</h3>
                  <p className="body-sm">A card with shadow for elevation.</p>
                </div>
              </div>

              <div className="card-interactive">
                <div className="card-body">
                  <h3 className="heading-5 mb-2">Interactive Card</h3>
                  <p className="body-sm">Hover to see the interaction effect.</p>
                </div>
              </div>
            </div>

            <div className="mt-8">
              <div className="card max-w-md">
                <div className="card-header">
                  <h3 className="heading-5">Card with Sections</h3>
                </div>
                <div className="card-body">
                  <p className="body-sm">This card demonstrates header, body, and footer sections.</p>
                </div>
                <div className="card-footer">
                  <button className="btn-primary btn-sm">Action</button>
                </div>
              </div>
            </div>
          </Section>

          {/* Badges Section */}
          <Section title="Badges">
            <div className="flex flex-wrap gap-4">
              <span className="badge-primary">Primary</span>
              <span className="badge-secondary">Secondary</span>
              <span className="badge-success">Success</span>
              <span className="badge-warning">Warning</span>
              <span className="badge-error">Error</span>
              <span className="badge-outline">Outline</span>
            </div>
          </Section>

          {/* Avatars Section */}
          <Section title="Avatars">
            <div className="flex flex-wrap gap-4 items-end">
              <div className="avatar avatar-xs">XS</div>
              <div className="avatar avatar-sm">SM</div>
              <div className="avatar avatar-md">MD</div>
              <div className="avatar avatar-lg">LG</div>
              <div className="avatar avatar-xl">XL</div>
            </div>
          </Section>

          {/* Upload Zone Section */}
          <Section title="Upload Zone">
            <div className="dropzone max-w-lg">
              <svg className="w-12 h-12 text-text-tertiary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <div className="text-center">
                <p className="body-base text-text-primary">Drag and drop images here</p>
                <p className="body-sm text-text-tertiary">or click to browse</p>
              </div>
            </div>
          </Section>

          {/* Skeleton Loading Section */}
          <Section title="Skeleton Loading">
            <div className="max-w-sm space-y-4">
              <div className="flex items-center gap-4">
                <div className="skeleton-avatar" />
                <div className="flex-1 space-y-2">
                  <div className="skeleton-text w-3/4" />
                  <div className="skeleton-text w-1/2" />
                </div>
              </div>
              <div className="skeleton-text" />
              <div className="skeleton-text w-5/6" />
              <div className="skeleton-button" />
            </div>
          </Section>

          {/* Gallery Grid Section */}
          <Section title="Gallery Grid">
            <div className="gallery-grid">
              {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
                <div key={i} className="gallery-item">
                  <div className="gallery-item-image bg-secondary-200" />
                  <div className="gallery-item-actions">
                    <span className="body-sm text-text-secondary truncate">image-{i}.jpg</span>
                    <div className="flex gap-2">
                      <button className="btn-icon btn-ghost btn-icon-sm">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </button>
                      <button className="btn-icon btn-ghost btn-icon-sm text-error-500">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Section>

          {/* Shadows Section */}
          <Section title="Shadows">
            <div className="flex flex-wrap gap-8">
              <div className="w-24 h-24 bg-surface-primary rounded-lg shadow-xs flex items-center justify-center">
                <span className="caption">XS</span>
              </div>
              <div className="w-24 h-24 bg-surface-primary rounded-lg shadow-sm flex items-center justify-center">
                <span className="caption">SM</span>
              </div>
              <div className="w-24 h-24 bg-surface-primary rounded-lg shadow-md flex items-center justify-center">
                <span className="caption">MD</span>
              </div>
              <div className="w-24 h-24 bg-surface-primary rounded-lg shadow-lg flex items-center justify-center">
                <span className="caption">LG</span>
              </div>
              <div className="w-24 h-24 bg-surface-primary rounded-lg shadow-xl flex items-center justify-center">
                <span className="caption">XL</span>
              </div>
              <div className="w-24 h-24 bg-surface-primary rounded-lg shadow-2xl flex items-center justify-center">
                <span className="caption">2XL</span>
              </div>
            </div>
          </Section>

          {/* Border Radius Section */}
          <Section title="Border Radius">
            <div className="flex flex-wrap gap-6">
              <div className="w-16 h-16 bg-primary-500 rounded-none flex items-center justify-center">
                <span className="text-white caption">none</span>
              </div>
              <div className="w-16 h-16 bg-primary-500 rounded-sm flex items-center justify-center">
                <span className="text-white caption">sm</span>
              </div>
              <div className="w-16 h-16 bg-primary-500 rounded flex items-center justify-center">
                <span className="text-white caption">def</span>
              </div>
              <div className="w-16 h-16 bg-primary-500 rounded-md flex items-center justify-center">
                <span className="text-white caption">md</span>
              </div>
              <div className="w-16 h-16 bg-primary-500 rounded-lg flex items-center justify-center">
                <span className="text-white caption">lg</span>
              </div>
              <div className="w-16 h-16 bg-primary-500 rounded-xl flex items-center justify-center">
                <span className="text-white caption">xl</span>
              </div>
              <div className="w-16 h-16 bg-primary-500 rounded-2xl flex items-center justify-center">
                <span className="text-white caption">2xl</span>
              </div>
              <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center">
                <span className="text-white caption">full</span>
              </div>
            </div>
          </Section>

          {/* Spacing Scale Section */}
          <Section title="Spacing Scale">
            <div className="flex flex-wrap gap-4 items-end">
              {[1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24].map((size) => (
                <div key={size} className="flex flex-col items-center gap-2">
                  <div
                    className="bg-primary-500"
                    style={{ width: `var(--spacing-${size})`, height: `var(--spacing-${size})` }}
                  />
                  <span className="caption">{size}</span>
                </div>
              ))}
            </div>
          </Section>
        </main>

        {/* Footer */}
        <footer className="border-t border-border-primary mt-16">
          <div className="max-w-6xl mx-auto px-6 py-8 text-center">
            <p className="body-sm">Image Hosting Design System</p>
          </div>
        </footer>
      </div>
    </div>
  );
}
