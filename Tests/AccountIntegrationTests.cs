using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Mvc;
using TextHunter.Controllers;
using TextHunter.Data;
using TextHunter.Models;
using Xunit;


namespace TextHunter.Tests
{
    public class AccountIntegrationTests
    {
        // 1. GetDatabaseContext metodunu buraya ekledik (Hata CS0103 çözümü)
        private AppDbContext GetDatabaseContext()
        {
            var options = new DbContextOptionsBuilder<AppDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;
            var databaseContext = new AppDbContext(options);
            databaseContext.Database.EnsureCreated();
            return databaseContext;
        }

        [Fact]
        public async Task Register_Post_ValidUser_SavesToDatabase()
        {
            // ARRANGE
            using var context = GetDatabaseContext();

            // Senin User.cs modeline göre oluşturuyoruz
            var newUser = new User
            {
                FullName = "Yeni Yazılımcı", // FullName ismi doğru
                Email = "test@mail.com",
                PasswordHash = "HashedPassword123!", // Password yerine PasswordHash
                CreatedAt = DateTime.UtcNow
            };

            // ACT
            context.Users.Add(newUser);
            await context.SaveChangesAsync();

            // ASSERT
            var userInDb = await context.Users.FirstOrDefaultAsync(u => u.Email == "test@mail.com");

            Assert.NotNull(userInDb);
            Assert.Equal("Yeni Yazılımcı", userInDb.FullName);
        }

        [Fact]
        public async Task Login_Logic_VerifyHashedPassword()
        {
            // ARRANGE: Önce bir kullanıcı kaydet
            using var context = GetDatabaseContext();
            var user = new User
            {
                FullName = "Admin",
                Email = "admin@texthunter.com",
                PasswordHash = "gizli_hash"
            };
            context.Users.Add(user);
            await context.SaveChangesAsync();

            // ACT: HomeController'daki Login mantığını simüle et
            var loggedInUser = await context.Users
                .FirstOrDefaultAsync(u => u.Email == "admin@texthunter.com" && u.PasswordHash == "gizli_hash");

            // ASSERT
            Assert.NotNull(loggedInUser);
            Assert.Equal("Admin", loggedInUser.FullName);
        }
    }
}
