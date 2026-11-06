import discord
from discord.ext import commands
import json
import os
import asyncio

if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        config = json.load(f)
        TOKEN = config.get("TOKEN")
        DEV_ID = config.get("DEV_ID", 1399721570888581151)
        PREFIX = config.get("PREFIX", "!")
else:
    TOKEN = "حط_توكن_البوت_هنا"
    DEV_ID = 1399721570888581151
    PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def is_developer():
    async def predicate(ctx):
        if ctx.author.id != DEV_ID:
            await ctx.send("❌ هذا الأمر خاص بمطور البوت الأساسي فقط!", delete_after=5)
            return False
        return True
    return commands.check(predicate)

class TicketButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="فتح تكت دعم فني 🎫", style=discord.ButtonStyle.green, custom_id="open_ticket_main")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="🎫 ── TICKETS")
        
        if not category:
            category = await guild.create_category("🎫 ── TICKETS")

        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{interaction.user.name.lower()}")
        if existing_channel:
            await interaction.response.send_message(f"❌ لديك تكت مفتوح بالفعل: {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        ticket_channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎫 تكت الدعم الفني - شينزو",
            description=f"أهلاً بك {interaction.user.mention}\nيرجى توضيح مشكلتك أو طلبك بالتفصيل، وسيتم الرد عليك من قِبل الإدارة قريباً.",
            color=discord.Color.from_rgb(43, 45, 49)
        )
        embed.set_footer(text="استخدم زر الإغلاق بالأسفل لإنهاء التكت.")

        await ticket_channel.send(embed=embed, view=TicketCloseView())
        await interaction.response.send_message(f"✅ تم إنشاء التكت الخاص بك بنجاح: {ticket_channel.mention}", ephemeral=True)

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="إغلاق التكت 🔒", style=discord.ButtonStyle.red, custom_id="close_ticket_btn")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏳ جاري إغلاق وحذف القناة خلال 3 ثوانٍ...")
        await asyncio.sleep(3)
        await interaction.channel.delete()

@bot.event
async def on_ready():
    print("========================================")
    print(f" [✓] Bot Logged in as: {bot.user}")
    print(f" [✓] Developer ID: {DEV_ID}")
    print(f" [✓] Status: Online 24/7 & Fully Operational")
    print("========================================")

@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎫 نظام التذاكر والدعم الفني",
        description="إذا احتجت لأي مساعدة، استفسار، أو تواجه مشكلة، اضغط على الزر بالأسفل لفتح تكت خاص مع الإدارة.",
        color=discord.Color.blue()
    )
    embed.set_footer(text="نظام شينزو البرمجي المتطور")
    await ctx.send(embed=embed, view=TicketButtonView())
    await ctx.message.delete()

@bot.command(name="dev_servers")
@is_developer()
async def dev_servers(ctx):
    servers_list = "\n".join([f"🔹 **{g.name}** (ID: `{g.id}`) ⟷ الأعضاء: `{g.member_count}`" for g in bot.guilds])
    if len(servers_list) > 1900:
        servers_list = servers_list[:1900] + "\n... (النص طويل جداً)"
    
    embed = discord.Embed(
        title="📊 إحصائيات سيرفرات البوت",
        description=servers_list,
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command(name="dev_leave")
@is_developer()
async def dev_leave(ctx, guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild:
        name = guild.name
        await guild.leave()
        await ctx.send(f"✅ تم مغادرة سيرفر **{name}** بنجاح.")
    else:
        await ctx.send("❌ لم يتم العثور على السيرفر بهذا الآي دي!")

@bot.command(name="dev_say")
@is_developer()
async def dev_say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

bot.run(MTU2ODI4NzI1ODYwNjMxMzU2Mw.GEiEQB.jYqR6sLoGL-Uv5kOrfRaxXkJuW-PWhUld0znh4)
