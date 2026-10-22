import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import View, Button

# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError(
        "TOKEN tidak ditemukan!\n"
        "Pastikan file .env berada di folder yang sama dengan bot.py"
    )

# ==========================================================
# DOR'S STORE CONFIG
# ==========================================================

BOT_NAME = "Dor's BOT"

GOLD = 0xD4AF37

# ==========================================================
# CHANNEL ID
# ==========================================================

WELCOME_CHANNEL_ID = 1515799357948039360
RULES_CHANNEL_ID = 1515944764900507831
VERIFY_CHANNEL_ID = 1515797614287913083
BOOST_CHANNEL_ID = 1515799048223985835

# ==========================================================
# SELF ROLE
# ==========================================================

SELF_ROLE_CHANNEL = VERIFY_CHANNEL_ID

CUSTOMER_ROLE = 1506561164958765086

# ==========================================================
# BOT INTENTS
# ==========================================================

intents = discord.Intents.default()

intents.guilds = True
intents.members = True
intents.message_content = True
intents.presences = True

# ==========================================================
# CREATE BOT
# ==========================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# ==========================================================
# CONSTANT
# ==========================================================

EMBED_FOOTER = "Dor's Store"

# ==========================================================
# SELF ROLE VIEW
# ==========================================================

class CustomerRoleView(View):

    def __init__(self):
        super().__init__(timeout=None)

        customer_button = Button(
            label="Customer",
            emoji="💎",
            style=discord.ButtonStyle.secondary,
            custom_id="customer_role"
        )

        customer_button.callback = self.customer_callback

        self.add_item(customer_button)

    async def customer_callback(
        self,
        interaction: discord.Interaction
    ):

        member = interaction.guild.get_member(
            interaction.user.id
        )

        role = interaction.guild.get_role(
            CUSTOMER_ROLE
        )

        if member is None:

            return await interaction.response.send_message(
                "❌ Member tidak ditemukan.",
                ephemeral=True
            )

        if role is None:

            return await interaction.response.send_message(
                "❌ Role Customer tidak ditemukan.",
                ephemeral=True
            )

        try:

            # ==========================================
            # REMOVE ROLE
            # ==========================================

            if role in member.roles:

                await member.remove_roles(role)

                embed = discord.Embed(
                    title="❌ Role Dihapus",
                    description=(
                        f"Role {role.mention} berhasil dihapus.\n\n"
                        "Kamu dapat mengambil role kembali kapan saja."
                    ),
                    color=discord.Color.red()
                )

                embed.set_footer(
                    text=EMBED_FOOTER
                )

                return await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )

            # ==========================================
            # ADD ROLE
            # ==========================================

            await member.add_roles(role)

            embed = discord.Embed(
                title="✅ Role Ditambahkan",
                description=(
                    f"Selamat datang di **Dor's Store** 👑\n\n"
                    f"Role {role.mention} berhasil ditambahkan.\n\n"
                    "Selamat berbelanja dan semoga nyaman berada di server kami."
                ),
                color=GOLD
            )

            embed.set_thumbnail(
                url=interaction.guild.icon.url
                if interaction.guild.icon
                else discord.Embed.Empty
            )

            embed.set_footer(
                text=EMBED_FOOTER
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                (
                    "❌ Bot tidak memiliki izin **Manage Roles**.\n\n"
                    "Pastikan:\n"
                    "• Role bot berada di atas role Customer.\n"
                    "• Bot memiliki permission Manage Roles."
                ),
                ephemeral=True
            )

        except Exception as e:

            await interaction.response.send_message(
                f"❌ Terjadi kesalahan:\n```{e}```",
                ephemeral=True
            )

# ==========================================================
# BOT READY
# ==========================================================

@bot.event
async def on_ready():

    # Persistent Self Role
    bot.add_view(CustomerRoleView())

    print("=" * 50)
    print("✅ LOGIN BERHASIL")
    print(f"🤖 Bot : {bot.user}")
    print(f"🆔 ID  : {bot.user.id}")
    print("=" * 50)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Dor's Store 👑"
        )
    )

    print("✅ Bot berhasil online.")

# ==========================================================
# WELCOME MESSAGE
# ==========================================================

@bot.event
async def on_member_join(member):

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if channel is None:
        print("❌ Welcome Channel tidak ditemukan.")
        return

    rules_channel = member.guild.get_channel(RULES_CHANNEL_ID)
    verify_channel = member.guild.get_channel(VERIFY_CHANNEL_ID)

    embed = discord.Embed(
        title="👋 Selamat Datang!",
        description=(
            f"Halo {member.mention}, selamat datang di **Dor's Store**.\n\n"
            "Silakan ikuti langkah berikut sebelum mulai beraktivitas:\n\n"
            f"📜 **Rules** : {rules_channel.mention}\n"
            f"✅ **Verification** : {verify_channel.mention}\n\n"
            "Semoga betah dan selamat berbelanja! 🛒"
        ),
        color=GOLD
    )

    embed.set_thumbnail(
        url=member.display_avatar.url
    )

    embed.set_footer(
        text=EMBED_FOOTER
    )

    try:
        await channel.send(embed=embed)

    except Exception as e:
        print(f"❌ Welcome Error : {e}")

# ==========================================================
# SERVER BOOST
# ==========================================================

@bot.event
async def on_member_update(before, after):

    # Member baru saja boost
    if before.premium_since is None and after.premium_since is not None:

        channel = bot.get_channel(BOOST_CHANNEL_ID)

        if channel is None:
            return

        embed = discord.Embed(
            title="🚀 Server Boost!",
            description=(
                f"{after.mention} baru saja melakukan **Server Boost**.\n\n"
                "Terima kasih atas dukunganmu untuk **Dor's Store**! 💎"
            ),
            color=GOLD
        )

        embed.set_thumbnail(
            url=after.display_avatar.url
        )

        embed.add_field(
            name="✨ Boost Level",
            value=f"Level **{after.guild.premium_tier}**",
            inline=False
        )

        embed.set_footer(
            text=EMBED_FOOTER
        )

        try:
            await channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Boost Error : {e}")

# ==========================================================
# COMMAND : PING
# ==========================================================

@bot.command(
    name="ping",
    help="Melihat latency bot."
)
async def ping(ctx):

    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        description=(
            f"**Latency :** `{latency} ms`\n\n"
            "Bot berjalan dengan normal."
        ),
        color=GOLD
    )

    embed.set_footer(
        text=EMBED_FOOTER
    )

    await ctx.send(embed=embed)


# ==========================================================
# COMMAND : SELF ROLE PANEL
# ==========================================================

@bot.command(
    name="selfrole",
    help="Mengirim panel Self Role."
)
@commands.has_permissions(administrator=True)
async def selfrole(ctx):

    channel = bot.get_channel(SELF_ROLE_CHANNEL)

    if channel is None:
        return await ctx.send(
            "❌ Channel Self Role tidak ditemukan."
        )

    embed = discord.Embed(
        description=(
            "## 📌 INFORMATION\n\n"
            "✅ **Ambil role** untuk mendapatkan akses penuh ke server.\n"
            "🛒 **Lihat produk** pada kategori **Store**.\n"
            "📜 **Wajib membaca Rules** sebelum melakukan transaksi.\n"
            "🎫 **Gunakan Ticket** apabila ingin mengorder sesuatu.\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "## 💎 CUSTOMER ROLE\n\n"
            "Tekan tombol **Customer** di bawah untuk\n"
            "mendapatkan atau menghapus role."
        ),
        color=GOLD
    )

    if bot.user.avatar:
        embed.set_thumbnail(
            url=bot.user.avatar.url
        )

    if ctx.guild.icon:
        embed.set_author(
            name=ctx.guild.name,
            icon_url=ctx.guild.icon.url
        )

    embed.set_footer(
        text="Dor's Store • Self Role"
    )

    await channel.send(
        embed=embed,
        view=CustomerRoleView()
    )

    success = discord.Embed(
        description="✅ Panel Self Role berhasil dikirim.",
        color=discord.Color.green()
    )

    await ctx.send(
        embed=success,
        delete_after=5
    )


# ==========================================================
# COMMAND ERROR
# ==========================================================

@selfrole.error
async def selfrole_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):

        embed = discord.Embed(
            title="❌ Permission Ditolak",
            description=(
                "Kamu harus memiliki permission "
                "**Administrator** untuk menggunakan command ini."
            ),
            color=discord.Color.red()
        )

        return await ctx.send(
            embed=embed,
            delete_after=8
        )

    raise error

# ==========================================================
# RUN BOT
# ==========================================================

if __name__ == "__main__":

    try:

        print("=" * 60)
        print(f"🚀 Menjalankan {BOT_NAME}")
        print("=" * 60)

        bot.run(TOKEN)

    except discord.LoginFailure:

        print("\n❌ TOKEN BOT INVALID")
        print("Silakan cek kembali TOKEN pada file .env")

    except KeyboardInterrupt:

        print("\n🛑 Bot dihentikan.")

    except Exception as e:

        print(f"\n❌ ERROR : {e}")