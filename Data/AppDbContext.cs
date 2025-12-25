using Microsoft.EntityFrameworkCore;
using TextHunter.Models;

namespace TextHunter.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<User> Users { get; set; }
        public DbSet<PredictionResultEntity> PredictionResults { get; set; }
    }
}
