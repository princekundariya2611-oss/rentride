import styles from './vehicles.module.css';
import Link from 'next/link';

// Mock Data for the demonstration before DB migration
const categories = [
  { name: 'All Categories', slug: '', icon: 'fa-solid fa-grip' },
  { name: 'Cars & SUVs', slug: 'cars', icon: 'fa-solid fa-car' },
  { name: 'Bikes & Scooters', slug: 'bikes', icon: 'fa-solid fa-motorcycle' },
];

const vehicles = [
  {
    id: 1,
    brand: 'Hyundai',
    name: 'Creta',
    category: { slug: 'cars', name: 'SUV' },
    location: 'Morbi',
    fuel_type: 'Petrol',
    transmission: 'Automatic',
    seats: 5,
    price_per_day: 2500,
    rating: 4.8,
    image: 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
  },
  {
    id: 2,
    brand: 'Royal Enfield',
    name: 'Classic 350',
    category: { slug: 'bikes', name: 'Cruiser' },
    location: 'Morbi',
    fuel_type: 'Petrol',
    transmission: 'Manual',
    seats: 2,
    price_per_day: 800,
    rating: 4.9,
    image: 'https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80',
  },
  {
    id: 3,
    brand: 'Mahindra',
    name: 'Thar',
    category: { slug: 'cars', name: 'SUV' },
    location: 'Morbi',
    fuel_type: 'Diesel',
    transmission: 'Manual',
    seats: 4,
    price_per_day: 3500,
    rating: 4.7,
    image: 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80',
  }
];

export default function VehiclesPage() {
  return (
    <main className={styles.main}>
      {/* 3D Header Banner */}
      <div className={styles.fleetHeroBanner}>
        <div className={styles.fleetBannerContent}>
          <div className={styles.sectionHeader}>
            <span className={styles.fleetHeroTag}>
              WheelX Inventory
            </span>
            <h1 className={styles.sectionTitle}>Explore Vehicles in Morbi</h1>
            <p className={styles.sectionDesc}>
              Filter by vehicle type, search your favorite brand, or sort by daily rental price with instant pickup in Morbi.
            </p>
          </div>
        </div>
      </div>

      <section className={styles.section}>
        <div className={styles.container}>
          {/* Search & Filter Controls (Glassmorphism) */}
          <div className={styles.filterGlassCard}>
            <form className={styles.filterForm}>
              <div className={styles.formGroup}>
                <label className={styles.formLabel}>Search Vehicle / Brand</label>
                <input 
                  type="text" 
                  name="q" 
                  className={styles.formControl} 
                  placeholder="Search Creta, Thar, Honda..." 
                />
              </div>
              <div className={styles.formGroup}>
                <label className={styles.formLabel}>Vehicle Type</label>
                <select name="type" className={styles.formControl}>
                  <option value="">All Types</option>
                  <option value="CAR">Cars & SUVs</option>
                  <option value="BIKE">Bikes & Scooters</option>
                </select>
              </div>
              <div className={styles.formGroup}>
                <label className={styles.formLabel}>Sort By</label>
                <select name="sort" className={styles.formControl}>
                  <option value="">Default</option>
                  <option value="price_low">Price: Low to High</option>
                  <option value="price_high">Price: High to Low</option>
                  <option value="rating">Highest Rated</option>
                </select>
              </div>
              <div className={styles.formGroup} style={{ justifyContent: 'flex-end', display: 'flex' }}>
                <button type="submit" className={styles.btnPrimary}>
                  Filter Fleet
                </button>
              </div>
            </form>
          </div>

          {/* Category Pills */}
          <div className={styles.categoryTabs}>
            {categories.map((cat, index) => (
              <Link 
                href={`#`} 
                key={index} 
                className={`${styles.tabBtn} ${index === 0 ? styles.active : ''}`}
              >
                {cat.name}
              </Link>
            ))}
          </div>

          {/* Fleet Grid */}
          <div className={styles.fleetGrid}>
            {vehicles.map((vehicle) => (
              <div key={vehicle.id} className={styles.vehicleCard}>
                <div className={styles.cardImgWrapper}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={vehicle.image} alt={vehicle.name} className={styles.cardImg} />
                  <span className={styles.cardBadge}>{vehicle.category.name}</span>
                  <span className={styles.cardRating}>★ {vehicle.rating}</span>
                </div>
                <div className={styles.cardBody}>
                  <h3 className={styles.vehicleTitle}>{vehicle.brand} {vehicle.name}</h3>
                  <div className={styles.vehicleLocation}>
                    📍 {vehicle.location}
                  </div>
                  <div className={styles.vehicleSpecs}>
                    <div className={styles.specItem}>
                      ⛽ <span>{vehicle.fuel_type}</span>
                    </div>
                    <div className={styles.specItem}>
                      ⚙️ <span>{vehicle.transmission}</span>
                    </div>
                    <div className={styles.specItem}>
                      👥 <span>{vehicle.seats} Seats</span>
                    </div>
                  </div>
                  <div className={styles.cardFooter}>
                    <div className={styles.priceTag}>
                      <span className={styles.amount}>₹{vehicle.price_per_day}</span>
                      <span className={styles.unit}>/ 24 hrs</span>
                    </div>
                    <Link href={`/vehicles/${vehicle.id}`} className={styles.btnPrimarySm}>
                      View Details
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
